(() => {
    "use strict";

    // 本文件负责页面交互与视图渲染；任务、配置和数据库等状态操作统一通过 PyWebView API 完成。
    const body = document.body;
    const content = document.getElementById("mainContent");
    const viewTitle = document.getElementById("viewTitle");
    const toastRegion = document.getElementById("toastRegion");
    const startupScreen = document.getElementById("startupScreen");

    const viewNames = new Set(["new_task", "monitor", "queue", "history", "logs", "settings", "disclaimer", "about"]);

    let uiTranslations = Object.create(null);
    let translatedUiInitialized = false;
    let aboutLinks = Object.create(null);

    function translateText(key) {
        return uiTranslations[key];
    }

    function formatTranslated(key, values = []) {
        // 替换 {0}、{1} 形式的占位符，统计数据由调用方传入。
        return translateText(key).replace(/\{(\d+)}/g, (match, index) => (
            values[Number(index)] ?? match
        ));
    }

    function applyStaticTranslations() {
        // 根据当前语言包更新 HTML 中标记 data-i18n 的文本及属性。
        document.querySelectorAll("[data-i18n]").forEach((element) => {
            element.textContent = translateText(element.dataset.i18n);
        });
        const attributeKeys = {
            placeholder: "i18nPlaceholder",
            title: "i18nTitle",
        };
        Object.entries(attributeKeys).forEach(([attribute, dataKey]) => {
            document.querySelectorAll(`[data-i18n-${attribute}]`).forEach((element) => {
                element.setAttribute(attribute, translateText(element.dataset[dataKey]));
            });
        });
    }

    function icon(name) {
        return `<svg><use href="#${name}"/></svg>`;
    }

    function showToast(text, type = "success") {
        // 提示消息仅用于短暂反馈，不保存业务状态；业务状态由后端快照负责同步。
        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <span class="toast-icon">${icon(type === "warning" ? "info" : "check")}</span>
            <span class="toast-message"></span>
        `;
        toast.querySelector(".toast-message").textContent = text;
        toastRegion.appendChild(toast);
        window.setTimeout(() => {
            toast.classList.add("out");
            window.setTimeout(() => toast.remove(), 200);
        }, 5000);
    }

    function closeSidebar() {
        // 移动端侧栏通过 body 的状态类控制显示和隐藏。
        body.classList.remove("sidebar-open");
    }

    let monitorMode = false;

    function updateViewHeader(name) {
        viewTitle.textContent = translateText(`nav.${name}`);
    }

    function setView(name, options = {}) {
        if (!viewNames.has(name)) return;
        // 监听运行期间锁定其他页面，避免在监听模式下修改配置或创建冲突任务。
        if (monitorMode && name !== "monitor" && !options.force) {
            return;
        }
        const page = document.querySelector(`.view[data-page="${name}"]`);
        if (!page) return;

        document.querySelectorAll(".view").forEach((item) => item.classList.toggle("active", item === page));
        document.querySelectorAll(".nav-item")
                .forEach((item) => item.classList.toggle("active", item.dataset.view === name));
        updateViewHeader(name);
        if (window.location.hash !== `#${name}`) {
            window.history.replaceState(null, "", `#${name}`);
        }
        content.scrollTop = 0;
        if (name === "settings") {
            window.requestAnimationFrame(updateSettingsNavigation);
        }
        closeSidebar();
    }

    // 普通导航和页面内跳转统一调用 setView，确保标题、URL hash 和侧栏状态保持一致。
    document.querySelectorAll("[data-view]").forEach((button) => {
        button.addEventListener("click", () => setView(button.dataset.view));
    });

    document.querySelectorAll("[data-go]").forEach((button) => {
        button.addEventListener("click", () => setView(button.dataset.go));
    });

    document.getElementById("mobileMenu").addEventListener("click", () => body.classList.add("sidebar-open"));
    document.getElementById("sidebarClose").addEventListener("click", closeSidebar);
    document.getElementById("sidebarScrim").addEventListener("click", closeSidebar);

    const monitorToggleButton = document.getElementById("monitorToggleButton");
    const monitorState = document.getElementById("monitorState");
    const monitorEvents = document.getElementById("monitorEvents");
    const monitorQueueEmpty = document.getElementById("monitorQueueEmpty");
    const monitorFileDownloadList = document.getElementById("monitorFileDownloadList");

    function renderMonitorState(active) {
        // 监听页始终显示当前状态；active 仅控制按钮和状态指示，不影响队列展示。
        monitorToggleButton.className = active ? "secondary-button danger-subtle" : "primary-button";
        monitorToggleButton.innerHTML = active
                                        ? `${icon("x")}${translateText("monitor.stop")}`
                                        : `${icon("play")}${translateText("monitor.start")}`;
        monitorState.classList.toggle("inactive", !active);
        monitorState.innerHTML = `<i></i><span>${translateText(active ? "monitor.active" : "monitor.inactive")}</span>`;
    }

    monitorToggleButton.addEventListener("click", () => {
        void runNativeAction(async () => {
            if (monitorMode) await nativeApi.stop_monitor();
            else await nativeApi.start_monitor();
        });
    });

    const disclaimerModal = document.getElementById("disclaimerModal");
    const recordModal = document.getElementById("recordModal");

    document.querySelectorAll("[data-close-modal]").forEach((button) => {
        button.addEventListener("click", () => button.closest("dialog").close());
    });

    document.querySelectorAll("dialog").forEach((dialog) => {
        dialog.addEventListener("cancel", (event) => {
            if (dialog.dataset.blocking === "true") event.preventDefault();
        });
        dialog.addEventListener("click", (event) => {
            if (dialog.dataset.blocking === "true") return;
            if (event.target === dialog) dialog.close();
        });
    });

    // 更新检查的网络请求由后端执行，前端负责显示检查状态、结果和错误反馈。
    const pageCheckUpdate = document.getElementById("pageCheckUpdate");
    const aboutUpdateResult = document.getElementById("aboutUpdateResult");

    function setUpdateResult(message = "", tone = "info") {
        aboutUpdateResult.hidden = !message;
        aboutUpdateResult.dataset.tone = tone;
        aboutUpdateResult.querySelector("span").textContent = message;
    }

    function setUpdateChecking(checking) {
        pageCheckUpdate.disabled = checking;
        pageCheckUpdate.classList.toggle("is-loading", checking);
        pageCheckUpdate.innerHTML = `${icon("refresh")}${translateText("update.check")}`;
    }

    // 创建任务区域只提交原始输入，作品链接提取和下载规则均由后端处理。
    const urlInput = document.getElementById("urlInput");
    const createTask = document.getElementById("createTask");

    function updateCreateButton() {
        const hasContent = Boolean(urlInput.value.trim());
        createTask.disabled = !hasContent;
        return hasContent;
    }

    function insertTextAtCursor(input, text) {
        const start = input.selectionStart ?? input.value.length;
        const end = input.selectionEnd ?? start;
        input.value = `${input.value.slice(0, start)}${text}${input.value.slice(end)}`;
        const cursor = start + text.length;
        input.setSelectionRange(cursor, cursor);
        updateCreateButton();
    }

    urlInput.addEventListener("input", updateCreateButton);

    urlInput.addEventListener("keydown", (event) => {
        if (!(event.key?.toLowerCase() === "v" && (event.ctrlKey || event.metaKey))) return;
        const previousValue = urlInput.value;
        window.setTimeout(() => {
            if (urlInput.value !== previousValue) return;
            void runNativeAction(async () => {
                const content = await nativeApi.paste_content();
                if (!content) return;
                insertTextAtCursor(urlInput, content);
                urlInput.focus();
            });
        });
    });

    document.getElementById("clearInput").addEventListener("click", () => {
        urlInput.value = "";
        updateCreateButton();
        urlInput.focus();
    });

    document.getElementById("pasteButton").addEventListener("click", () => {
        void runNativeAction(async () => {
            const content = await nativeApi.paste_content();
            if (content) insertTextAtCursor(urlInput, content);
            urlInput.focus();
        });
    });

    createTask.addEventListener("click", () => {
        void runNativeAction(async () => {
            const created = await nativeApi.create_tasks(urlInput.value);
            if (!created.length) throw new Error(translateText("toast.no_supported_link"));
            urlInput.value = "";
            updateCreateButton();
        });
    });
    document.getElementById("pasteAndProcess").addEventListener("click", () => {
        void runNativeAction(async () => {
            const content = await nativeApi.paste_content();
            urlInput.value = content;
            updateCreateButton();
            const created = await nativeApi.create_tasks(content);
            if (!created.length) throw new Error(translateText("toast.no_supported_link"));
            urlInput.value = "";
            updateCreateButton();
        });
    });

    // 任务队列和文件下载区使用独立的滚动容器，避免条目增加时改变页面整体高度。
    const queueList = document.getElementById("queueList");
    const queueEmpty = document.getElementById("queueEmpty");
    const fileDownloadList = document.getElementById("fileDownloadList");
    let currentQueueFilter = "all";

    const listScrollStates = new WeakMap();

    function isNearBottom(target, threshold = 2) {
        return target.scrollHeight - target.scrollTop - target.clientHeight <= threshold;
    }

    function followsBottom(target) {
        let state = listScrollStates.get(target);
        if (state) return state.followBottom;
        state = {followBottom: true};
        target.addEventListener("scroll", () => {
            state.followBottom = isNearBottom(target);
        });
        listScrollStates.set(target, state);
        return state.followBottom;
    }

    function stickToBottom(target, enabled) {
        if (!enabled) return;
        target.scrollTop = target.scrollHeight;
    }

    function matchesQueueFilter(state, filter = currentQueueFilter) {
        // 筛选仅修改当前视图的 hidden 状态，不会从后端任务集合中删除任务。
        if (filter === "all") return true;
        if (filter === "processing") return state === "processing";
        return state === filter;
    }

    function refreshQueue() {
        // 根据后端快照生成的 DOM 统计各状态数量，并更新筛选结果为空时的提示。
        const items = [...queueList.querySelectorAll(".queue-item")];
        const counts = items.reduce((result, item) => {
            result[item.dataset.state] += 1;
            item.hidden = !matchesQueueFilter(item.dataset.state);
            return result;
        }, {
                                        processing: 0,
                                        pending: 0,
                                        success: 0,
                                        failed: 0,
                                        skipped: 0,
                                    });
        const processing = counts.processing;
        const pending = counts.pending;
        const success = counts.success;
        const failed = counts.failed;
        const skipped = counts.skipped;
        const visible = items.filter((item) => !item.hidden).length;

        document.getElementById("pendingMetric").innerHTML = `${pending} <small>${translateText("unit.item")}</small>`;
        document.getElementById("successMetric").innerHTML = `${success} <small>${translateText("unit.item")}</small>`;
        document.getElementById("failedMetric").innerHTML = `${failed} <small>${translateText("unit.item")}</small>`;
        document.getElementById("skippedMetric").innerHTML = `${skipped} <small>${translateText("unit.item")}</small>`;
        document.getElementById("queueBadge").textContent = String(processing + pending);
        queueEmpty.querySelector("strong").textContent = translateText(
            currentQueueFilter === "all" ? "task.queue_empty" : "queue.current_filter_empty",
        );
        queueList.hidden = visible === 0;
        queueEmpty.hidden = visible !== 0;
    }

    document.getElementById("queueFilters").addEventListener("click", (event) => {
        const button = event.target.closest("[data-filter]");
        if (!button) return;
        currentQueueFilter = button.dataset.filter;
        document.querySelectorAll("#queueFilters button")
                .forEach((item) => item.classList.toggle("active", item === button));
        refreshQueue();
    });

    let currentMonitorFilter = "all";

    function refreshMonitorQueue() {
        // 监听页仅展示 source=monitor 的任务，状态筛选规则与主队列保持一致。
        const items = [...monitorEvents.querySelectorAll(".queue-item")];
        items.forEach((item) => {
            item.hidden = !matchesQueueFilter(item.dataset.state, currentMonitorFilter);
        });
        const visible = items.filter((item) => !item.hidden).length;
        monitorQueueEmpty.querySelector("strong").textContent = translateText(
            currentMonitorFilter === "all" ? "monitor.queue_empty" : "queue.current_filter_empty",
        );
        monitorEvents.hidden = visible === 0;
        monitorQueueEmpty.hidden = visible !== 0;
    }

    document.getElementById("monitorQueueFilters").addEventListener("click", (event) => {
        const button = event.target.closest("[data-filter]");
        if (!button) return;
        currentMonitorFilter = button.dataset.filter;
        document.querySelectorAll("#monitorQueueFilters button")
                .forEach((item) => item.classList.toggle("active", item === button));
        refreshMonitorQueue();
    });

    // 下载记录仅包含作品 ID；搜索、总数和分页信息均由数据库查询结果决定。
    const historySearch = document.getElementById("historySearch");
    const historyBody = document.getElementById("historyBody");
    const historyEmpty = document.getElementById("historyEmpty");
    const selectAllRecords = document.getElementById("selectAllRecords");
    const invertRecordSelection = document.getElementById("invertRecordSelection");
    const deleteSelectedRecords = document.getElementById("deleteSelectedRecords");
    const selectedRecordCount = document.getElementById("selectedRecordCount");
    const historyPrev = document.getElementById("historyPrev");
    const historyNext = document.getElementById("historyNext");
    const historyPageLabel = document.getElementById("historyPage");
    const historyView = document.querySelector(".history-view");
    let historyPageSize = 0;
    let historyPage = 1;
    let historyPageCount = 0;
    let historyTotal = 0;
    let historyQuery = "";
    let historyEnabled = true;
    let historyRequestId = 0;
    let historySearchTimer = null;
    let lastHistoryRevision = null;

    function recordRows() {
        return [...historyBody.querySelectorAll(".history-record")];
    }

    function selectedHistoryIds() {
        return recordRows()
            .filter((row) => row.querySelector(".record-select").checked)
            .map((row) => row.querySelector("code").textContent);
    }

    function updateRecordSummary() {
        const rows = recordRows();
        const start = historyTotal ? ((historyPage - 1) * historyPageSize) + 1 : 0;
        const end = historyTotal ? start + rows.length - 1 : 0;
        document.getElementById("recordRange").textContent = !historyEnabled
                                                             ? ""
                                                             : historyTotal
                                                               ? formatTranslated(
                    "history.range",
                    [start, end, historyTotal,
                     historyQuery ? translateText(
                         "history.search_results") : ""]
                )
                                                               : historyQuery ? translateText("history.no_match") :
                                                                 translateText("history.empty");
        historyPageLabel.textContent = historyPageCount ? `${historyPage} / ${historyPageCount}` : "0 / 0";
        historyPrev.disabled = !historyEnabled || !historyPageCount || historyPage <= 1;
        historyNext.disabled = !historyEnabled || !historyPageCount || historyPage >= historyPageCount;
    }

    function updateRecordSelection() {
        // 选择状态仅属于当前页，不跨页保存；删除选中记录必须经过确认对话框。
        const rows = recordRows();
        const selectedRows = rows.filter((row) => row.querySelector(".record-select").checked);

        rows.forEach((row) => {
            const selected = row.querySelector(".record-select").checked;
            row.classList.toggle("selected", selected);
        });
        selectAllRecords.checked = rows.length > 0 && selectedRows.length === rows.length;
        selectAllRecords.indeterminate = selectedRows.length > 0 && selectedRows.length < rows.length;
        selectAllRecords.disabled = !historyEnabled || rows.length === 0;
        invertRecordSelection.disabled = !historyEnabled || rows.length === 0;
        selectedRecordCount.textContent = formatTranslated("history.selected", [selectedRows.length]);
        deleteSelectedRecords.disabled = !historyEnabled || selectedRows.length === 0;
        updateRecordSummary();
    }

    function setHistoryEnabled(enabled) {
        // 下载记录关闭后，整个记录视图进入只读禁用状态，禁止继续调用数据库接口。
        historyEnabled = Boolean(enabled);
        historyView.classList.toggle("is-disabled", !historyEnabled);
        historySearch.disabled = !historyEnabled;
        if (!historyEnabled) {
            historyRequestId += 1;
            historyBody.replaceChildren();
            historyBody.hidden = true;
            historyEmpty.hidden = false;
            historyEmpty.querySelector("strong").textContent = translateText("history.disabled");
            historyTotal = 0;
            historyPage = 0;
            historyPageCount = 0;
            historyQuery = "";
            historySearch.value = "";
        }
        updateRecordSelection();
    }

    function renderNativeHistoryPage(result) {
        // 后端每次最多返回 100 个 ID，前端负责生成紧凑且可整体选中的记录行。
        setHistoryEnabled(result.enabled !== false);
        if (!historyEnabled) return;
        historyTotal = Number(result.total);
        historyPage = Number(result.page);
        historyPageSize = Number(result.page_size);
        historyPageCount = Number(result.page_count);
        historyQuery = String(result.query);
        historyBody.replaceChildren();
        result.items.forEach((id) => {
            const row = document.createElement("li");
            row.className = "history-record";
            row.tabIndex = 0;
            const label = document.createElement("span");
            label.className = "record-checkbox";
            const checkbox = document.createElement("input");
            checkbox.className = "record-select";
            checkbox.type = "checkbox";
            checkbox.tabIndex = -1;
            const mark = document.createElement("span");
            mark.className = "checkmark";
            mark.innerHTML = icon("check");
            label.append(checkbox, mark);
            const code = document.createElement("code");
            code.textContent = id;
            row.append(label, code);
            historyBody.append(row);
        });
        const hasRows = recordRows().length > 0;
        historyEmpty.hidden = hasRows;
        historyEmpty.querySelector("strong").textContent = translateText(
            historyQuery ? "history.no_match" : "history.empty");
        historyBody.hidden = !hasRows;
        updateRecordSelection();
    }

    async function requestHistoryPage(page = 1) {
        // 通过 requestId 丢弃过期的搜索请求，防止慢响应覆盖较新的查询结果。
        if (!historyEnabled) return;
        const requestId = ++historyRequestId;
        const query = historySearch.value.trim();
        try {
            const result = await nativeApi.get_history_page(query, page);
            if (requestId !== historyRequestId) return;
            renderNativeHistoryPage(result);
        } catch (error) {
            if (requestId === historyRequestId) showToast(
                translateText("history.read_failed"), "warning");
        }
    }

    historySearch.addEventListener("input", () => {
        window.clearTimeout(historySearchTimer);
        historySearchTimer = window.setTimeout(() => {
            void requestHistoryPage(1);
        }, 250);
    });

    historyPrev.addEventListener("click", () => {
        if (historyPage <= 1) return;
        void requestHistoryPage(historyPage - 1);
    });

    historyNext.addEventListener("click", () => {
        if (historyPage >= historyPageCount) return;
        void requestHistoryPage(historyPage + 1);
    });

    function toggleHistoryRow(row) {
        if (!historyEnabled || !row) return;
        const checkbox = row.querySelector(".record-select");
        checkbox.checked = !checkbox.checked;
        updateRecordSelection();
    }

    historyBody.addEventListener("click", (event) => {
        const row = event.target.closest(".history-record");
        if (!row) return;
        event.preventDefault();
        toggleHistoryRow(row);
    });

    historyBody.addEventListener("keydown", (event) => {
        if (event.key !== " " && event.key !== "Enter") return;
        const row = event.target.closest(".history-record");
        if (!row) return;
        event.preventDefault();
        toggleHistoryRow(row);
    });

    selectAllRecords.addEventListener("change", () => {
        recordRows().forEach((row) => {
            row.querySelector(".record-select").checked = selectAllRecords.checked;
        });
        updateRecordSelection();
    });

    invertRecordSelection.addEventListener("click", () => {
        recordRows().forEach((row) => {
            const checkbox = row.querySelector(".record-select");
            checkbox.checked = !checkbox.checked;
        });
        updateRecordSelection();
    });

    deleteSelectedRecords.addEventListener("click", () => {
        const ids = selectedHistoryIds();
        if (!historyEnabled || ids.length === 0) return;
        document.getElementById("recordDeletePrompt").textContent = formatTranslated(
            "modal.delete_history_confirm", [ids.length]);
        recordModal.showModal();
    });

    const logConsole = document.getElementById("logConsole");

    // 设置导航仅滚动设置面板，避免改变整个窗口的滚动位置。
    const settingsPanel = document.getElementById("settingsPanel");
    const settingsNavButtons = [...document.querySelectorAll(".settings-nav button")];
    const settingsGroups = settingsNavButtons
        .map((button) => document.getElementById(button.dataset.setting))
        .filter(Boolean);
    let settingsScrollTarget = null;

    function setActiveSettingsGroup(groupId) {
        settingsNavButtons.forEach((button) => {
            button.classList.toggle("active", button.dataset.setting === groupId);
        });
    }

    function updateSettingsNavigation() {
        if (!settingsPanel || settingsGroups.length === 0 || settingsPanel.clientHeight === 0) return;

        const panelTop = settingsPanel.getBoundingClientRect().top;
        const atBottom = settingsPanel.scrollTop
            >= settingsPanel.scrollHeight - settingsPanel.clientHeight - 1;

        if (settingsScrollTarget) {
            const targetTop = settingsScrollTarget.getBoundingClientRect().top - panelTop;
            const targetIsLast = settingsScrollTarget === settingsGroups[settingsGroups.length - 1];
            if (Math.abs(targetTop) <= 1 || (targetIsLast && atBottom)) {
                settingsScrollTarget = null;
            } else {
                return;
            }
        }

        let activeGroup = settingsGroups[0];

        if (atBottom) {
            activeGroup = settingsGroups[settingsGroups.length - 1];
        } else {
            settingsGroups.forEach((group) => {
                if (group.getBoundingClientRect().top <= panelTop + 24) {
                    activeGroup = group;
                }
            });
        }
        setActiveSettingsGroup(activeGroup.id);
    }

    settingsNavButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const target = document.getElementById(button.dataset.setting);
            if (!target) return;
            settingsScrollTarget = target;
            setActiveSettingsGroup(button.dataset.setting);
            const top = target.getBoundingClientRect().top - settingsPanel.getBoundingClientRect().top + settingsPanel.scrollTop;
            settingsPanel.scrollTo({top, behavior: "smooth"});
        });
    });
    settingsPanel?.addEventListener("wheel", () => {
        settingsScrollTarget = null;
    }, {passive: true});
    settingsPanel?.addEventListener("touchstart", () => {
        settingsScrollTarget = null;
    }, {passive: true});
    settingsPanel?.addEventListener("scroll", updateSettingsNavigation, {passive: true});
    window.addEventListener("resize", updateSettingsNavigation);

    // 文件命名字段可在“启用”和“未启用”两栏之间拖拽，启用栏顺序即配置保存顺序。
    let NAME_FORMAT_FIELDS = [];
    const enabledNameFields = document.getElementById("enabledNameFields");
    const disabledNameFields = document.getElementById("disabledNameFields");
    let draggedNameField = null;
    let nameFieldWasDragged = false;
    let pointerNameDrag = null;

    function updateNameFormatCounts() {
        document.getElementById("enabledNameFieldCount").textContent = String(enabledNameFields.children.length);
        document.getElementById("disabledNameFieldCount").textContent = String(disabledNameFields.children.length);
    }

    function placeNameFormatToken(zone, target, clientX, clientY) {
        if (!target || target === draggedNameField) {
            zone.append(draggedNameField);
            return;
        }
        const bounds = target.getBoundingClientRect();
        const before = clientY < bounds.top + (bounds.height / 2)
            || (clientY <= bounds.bottom && clientX < bounds.left + (bounds.width / 2));
        zone.insertBefore(draggedNameField, before ? target : target.nextSibling);
    }

    function createNameFormatToken(field, enabled) {
        // 同时支持桌面 drag/drop 和触摸设备 pointer 拖拽；点击字段项可切换启用状态。
        const token = document.createElement("button");
        token.className = "name-format-token";
        token.type = "button";
        token.draggable = true;
        token.dataset.nameField = field;
        token.title = translateText(enabled ? "name.drag_disable" : "name.drag_enable");
        token.textContent = translateText(field);
        token.addEventListener("click", () => {
            if (nameFieldWasDragged) return;
            const target = token.parentElement === enabledNameFields ? disabledNameFields : enabledNameFields;
            target.append(token);
            token.title = translateText(target === enabledNameFields ? "name.drag_disable" : "name.drag_enable");
            updateNameFormatCounts();
        });
        token.addEventListener("dragstart", (event) => {
            draggedNameField = token;
            nameFieldWasDragged = true;
            event.dataTransfer.effectAllowed = "move";
            event.dataTransfer.setData("text/plain", field);
            window.setTimeout(() => token.classList.add("dragging"));
        });
        token.addEventListener("dragend", () => {
            token.classList.remove("dragging");
            document.querySelectorAll(".name-format-zone").forEach((zone) => zone.classList.remove("drag-over"));
            token.title = translateText(
                token.parentElement === enabledNameFields ? "name.drag_disable" : "name.drag_enable");
            draggedNameField = null;
            updateNameFormatCounts();
            window.setTimeout(() => {
                nameFieldWasDragged = false;
            });
        });
        token.addEventListener("pointerdown", (event) => {
            if (event.pointerType === "mouse") return;
            pointerNameDrag = {
                token,
                pointerId: event.pointerId,
                startX: event.clientX,
                startY: event.clientY,
                active: false,
            };
            token.setPointerCapture(event.pointerId);
        });
        token.addEventListener("pointermove", (event) => {
            if (!pointerNameDrag || pointerNameDrag.pointerId !== event.pointerId) return;
            const distance = Math.hypot(
                event.clientX - pointerNameDrag.startX,
                event.clientY - pointerNameDrag.startY,
            );
            if (!pointerNameDrag.active && distance < 8) return;
            event.preventDefault();
            pointerNameDrag.active = true;
            nameFieldWasDragged = true;
            draggedNameField = token;
            token.classList.add("dragging");
            const target = document.elementFromPoint(event.clientX, event.clientY);
            const zone = target?.closest(".name-format-zone");
            if (!zone) return;
            document.querySelectorAll(".name-format-zone")
                    .forEach((item) => item.classList.toggle("drag-over", item === zone));
            placeNameFormatToken(zone, target.closest(".name-format-token"), event.clientX, event.clientY);
        });
        const finishPointerDrag = (event) => {
            if (!pointerNameDrag || pointerNameDrag.pointerId !== event.pointerId) return;
            const wasActive = pointerNameDrag.active;
            token.classList.remove("dragging");
            document.querySelectorAll(".name-format-zone").forEach((zone) => zone.classList.remove("drag-over"));
            if (token.hasPointerCapture(event.pointerId)) token.releasePointerCapture(event.pointerId);
            pointerNameDrag = null;
            draggedNameField = null;
            updateNameFormatCounts();
            if (wasActive) window.setTimeout(() => {
                nameFieldWasDragged = false;
            });
        };
        token.addEventListener("pointerup", finishPointerDrag);
        token.addEventListener("pointercancel", finishPointerDrag);
        return token;
    }

    function applyNameFormat(value) {
        // 将配置中的空格分隔字段还原为两栏控件，并去除重复项及未知字段。
        const fields = String(value).split(/\s+/).filter((field, index, items) => (
            NAME_FORMAT_FIELDS.includes(field) && items.indexOf(field) === index
        ));
        const enabled = new Set(fields);
        enabledNameFields.replaceChildren(...fields.map((field) => createNameFormatToken(field, true)));
        disabledNameFields.replaceChildren(...NAME_FORMAT_FIELDS
            .filter((field) => !enabled.has(field))
            .map((field) => createNameFormatToken(field, false)));
        updateNameFormatCounts();
    }

    document.querySelectorAll(".name-format-zone").forEach((zone) => {
        zone.addEventListener("dragover", (event) => {
            if (!draggedNameField) return;
            event.preventDefault();
            event.dataTransfer.dropEffect = "move";
            zone.classList.add("drag-over");
            const target = event.target.closest(".name-format-token");
            placeNameFormatToken(zone, target, event.clientX, event.clientY);
        });
        zone.addEventListener("dragleave", (event) => {
            if (!zone.contains(event.relatedTarget)) zone.classList.remove("drag-over");
        });
        zone.addEventListener("drop", (event) => {
            event.preventDefault();
            zone.classList.remove("drag-over");
            updateNameFormatCounts();
        });
    });

    function initializeTranslatedUi() {
        refreshQueue();
        refreshMonitorQueue();
        updateRecordSelection();
        renderMonitorState(monitorMode);
        if (!translatedUiInitialized) {
            const initialView = window.location.hash.slice(1);
            setView(viewNames.has(initialView) ? initialView : "new_task");
            translatedUiInitialized = true;
        }
    }

    // PyWebView 负责所有数据变更，DOM 仅渲染快照；以下变量用于控制轮询和请求去重。
    let nativeApi = null;
    let bridgeRefreshBusy = false;
    let settingsLoaded = false;
    let lastLogKey = null;
    let stateRefreshTimer = null;

    const statusLabels = {
        processing: "queue.processing",
        pending: "queue.pending",
        success: "queue.success",
        failed: "queue.failed",
        skipped: "queue.skipped",
        cancelled: "queue.cancelled",
    };

    function statusClass(state) {
        // 将后端状态映射为 CSS 状态类，显示文案由 statusLabels 映射到翻译键。
        if (state === "success") return "completed";
        if (state === "failed") return "failed";
        if (state === "skipped") return "skipped";
        if (state === "processing") return "downloading";
        return "waiting";
    }

    function formatBytes(value) {
        // 文件进度固定使用 MB；总大小未知时由调用方显示“未知大小”。
        if (!Number.isFinite(value) || value <= 0) return "0.00MB";
        return `${(value / (1024 ** 2)).toFixed(2)} MB`;
    }

    function createNativeQueueItem(task) {
        // 根据后端任务快照创建主队列条目；仅 pending 任务显示取消按钮。
        const item = document.createElement("article");
        item.className = "queue-item";
        item.dataset.state = task.state;
        item.dataset.taskId = task.task_id;

        const symbol = document.createElement("span");
        symbol.className = "queue-symbol";
        symbol.innerHTML = icon("link");
        const detail = document.createElement("div");
        detail.className = "queue-detail";
        const link = document.createElement("code");
        link.textContent = task.url;
        link.title = task.url;
        const stateLine = document.createElement("div");
        stateLine.className = "queue-state-line";
        const state = document.createElement("span");
        state.className = `status-text ${statusClass(task.state)}`;
        state.textContent = translateText(statusLabels[task.state]);
        stateLine.append(state);
        detail.append(link, stateLine);
        item.append(symbol, detail);
        if (task.state === "pending") {
            const actions = document.createElement("div");
            actions.className = "queue-actions";
            const cancel = document.createElement("button");
            cancel.className = "icon-button danger-icon";
            cancel.type = "button";
            cancel.dataset.action = "cancel";
            cancel.innerHTML = icon("x");
            actions.append(cancel);
            item.append(actions);
        }
        return item;
    }

    function createNativeCompactTask(task) {
        // 首页显示紧凑的任务摘要，完整链接和状态在处理队列页查看。
        const item = document.createElement("article");
        item.className = "compact-task";
        const symbol = document.createElement("span");
        symbol.className = "queue-symbol";
        symbol.innerHTML = icon("link");
        const primary = document.createElement("div");
        primary.className = "task-primary";
        const link = document.createElement("code");
        link.textContent = task.url;
        primary.append(link);
        const state = document.createElement("span");
        state.className = `status-text ${statusClass(task.state)}`;
        if (task.state === "success") state.innerHTML = icon("check");
        else state.append(document.createElement("i"));
        state.append(document.createTextNode(translateText(statusLabels[task.state])));
        item.append(symbol, primary, state);
        return item;
    }

    function renderNativeFiles(target, files) {
        // 每个文件独立显示名称、已完成大小、总大小和实时进度条；列表容器负责滚动。
        const shouldStickToBottom = followsBottom(target);
        target.replaceChildren();
        if (!files.length) {
            const empty = document.createElement("div");
            empty.className = "file-download-empty";
            empty.innerHTML = `${icon("download")}<span>${translateText("download.empty")}</span>`;
            target.append(empty);
        }
        files.forEach((file) => {
            const row = document.createElement("article");
            row.className = "file-download-row";
            const head = document.createElement("div");
            head.className = "file-download-head";
            const name = document.createElement("strong");
            name.textContent = file.filename;
            name.title = file.filename;
            const meta = document.createElement("div");
            meta.className = "file-download-meta";
            const size = document.createElement("span");
            const completed = formatBytes(Number(file.completed_bytes));
            const total = file.total_bytes ? formatBytes(Number(file.total_bytes)) :
                          translateText("download.unknown_size");
            const percent = file.total_bytes ? Math.min(100, (file.completed_bytes / file.total_bytes) * 100) : 0;
            const progress = document.createElement("span");
            size.textContent = file.total_bytes ? `${completed}/${total}` : completed;
            progress.textContent = file.total_bytes ? `${Math.round(percent)}%` : "";
            meta.append(size, progress);
            head.append(name, meta);
            const line = document.createElement("div");
            line.className = `progress-line file ${file.state === "completed" ? "completed" : ""}`;
            const fill = document.createElement("i");
            fill.style.width = `${percent}%`;
            line.append(fill);
            row.append(head, line);
            target.append(row);
        });
        const count = target.closest(".file-download-section")?.querySelector(".section-heading span");
        if (count) count.textContent = `${files.length} ${translateText("unit.file")}`;
        stickToBottom(target, shouldStickToBottom);
    }

    function renderNativeTaskLists(tasks, files) {
        // 使用一次状态快照同时刷新主队列、监听队列及两个文件下载区域。
        const visibleTasks = tasks.filter((task) => task.state !== "cancelled");
        const queueShouldStickToBottom = followsBottom(queueList);
        const monitorShouldStickToBottom = followsBottom(monitorEvents);
        queueList.replaceChildren(...visibleTasks.map(createNativeQueueItem));
        const dashboardTasks = document.getElementById("dashboardTasks");
        const dashboardShouldStickToBottom = followsBottom(dashboardTasks);
        if (visibleTasks.length) {
            dashboardTasks.replaceChildren(...visibleTasks.map(createNativeCompactTask));
        } else {
            const empty = document.createElement("div");
            empty.className = "dashboard-empty";
            empty.textContent = translateText("task.queue_empty");
            dashboardTasks.replaceChildren(empty);
        }
        stickToBottom(dashboardTasks, dashboardShouldStickToBottom);
        document.getElementById("dashboardTaskCount").textContent = `${visibleTasks.length} ${translateText(
            "unit.item")}`;
        const monitorTasks = visibleTasks.filter((task) => task.source === "monitor");
        monitorEvents.replaceChildren(...monitorTasks.map(createNativeQueueItem));
        const monitorIds = new Set(monitorTasks.map((task) => task.task_id));
        renderNativeFiles(fileDownloadList, files);
        renderNativeFiles(monitorFileDownloadList, files.filter((file) => monitorIds.has(file.task_id)));
        refreshQueue();
        refreshMonitorQueue();
        stickToBottom(queueList, queueShouldStickToBottom && !queueList.hidden);
        stickToBottom(monitorEvents, monitorShouldStickToBottom && !monitorEvents.hidden);
    }

    function renderNativeLogs(logs) {
        // 通过 JSON 快照去重，避免每 500 ms 轮询都重建未发生变化的日志节点。
        const key = JSON.stringify(logs);
        if (key === lastLogKey) return;
        lastLogKey = key;
        logConsole.replaceChildren();
        logs.forEach((entry) => {
            const line = document.createElement("div");
            line.dataset.level = entry.level;
            const time = document.createElement("time");
            time.textContent = entry.time;
            const level = document.createElement("span");
            level.className = `log-level ${entry.level}`;
            level.textContent = entry.level.toUpperCase();
            const message = document.createElement("p");
            message.textContent = entry.message;
            line.append(time, level, message);
            logConsole.append(line);
        });
    }

    function applyNativeSettings(settings) {
        // 首次接收后端配置时填充表单；用户编辑后不再被轮询覆盖。
        if (settingsLoaded) return;
        document.getElementById("settingsWorkPath").value = settings.work_path;
        document.getElementById("settingsFolderName").value = settings.folder_name;
        applyNameFormat(settings.name_format);
        document.getElementById("settingsImageDownload").checked = Boolean(settings.image_download);
        document.getElementById("settingsVideoDownload").checked = Boolean(settings.video_download);
        document.getElementById("settingsLiveDownload").checked = Boolean(settings.live_download);
        document.getElementById("settingsImageFormat").value = settings.image_format.toLowerCase();
        document.getElementById("settingsVideoPreference").value = settings.video_preference;
        document.getElementById("settingsNoteFormat").value = settings.note_format;
        document.getElementById("settingsFolderMode").checked = Boolean(settings.folder_mode);
        document.getElementById("settingsAuthorArchive").checked = Boolean(settings.author_archive);
        document.getElementById("settingsDownloadRecord").checked = Boolean(settings.download_record);
        document.getElementById("settingsRecordData").checked = Boolean(settings.record_data);
        document.getElementById("settingsWriteMtime").checked = Boolean(settings.write_mtime);
        document.getElementById("settingsCookie").value = settings.cookie || "";
        document.getElementById("settingsUserAgent").value = settings.user_agent || "";
        document.getElementById("settingsProxy").value = settings.proxy || "";
        document.getElementById("settingsTimeout").value = String(settings.timeout);
        document.getElementById("settingsMaxRetry").value = String(settings.max_retry);
        document.getElementById("settingsChunkSize").value = String(settings.chunk);
        document.getElementById("settingsLanguage").value = settings.language;
        document.getElementById("settingsScriptServer").checked = Boolean(settings.script_server);
        settingsLoaded = true;
    }

    async function refreshUiTranslations() {
        // 保存语言设置后重新获取完整文案，并重建依赖翻译的动态控件。
        const payload = await nativeApi.get_translations();
        uiTranslations = Object.assign(Object.create(null), payload.messages);
        NAME_FORMAT_FIELDS = payload.name_fields;
        document.documentElement.lang = payload.language === "en_US" ? "en" : "zh-CN";
        applyStaticTranslations();
        const nameFormat = [...enabledNameFields.children]
            .map((token) => token.dataset.nameField)
            .join(" ");
        applyNameFormat(nameFormat);
        const activeView = document.querySelector(".view.active")?.dataset.page;
        if (viewNames.has(activeView)) {
            updateViewHeader(activeView);
        }
        initializeTranslatedUi();
    }

    function collectNativeSettings() {
        // 提交当前语言的字段显示名称；后端负责将英文名称还原为中文配置值。
        const nameFormat = [...enabledNameFields.children]
            .map((token) => token.textContent.trim());
        const chunkSize = Math.max(
            1, Number.parseInt(document.getElementById("settingsChunkSize").value, 10) || 2097152);
        return {
            work_path: document.getElementById("settingsWorkPath").value.trim(),
            folder_name: document.getElementById("settingsFolderName").value.trim() || "Download",
            name_format: nameFormat,
            image_download: document.getElementById("settingsImageDownload").checked,
            video_download: document.getElementById("settingsVideoDownload").checked,
            live_download: document.getElementById("settingsLiveDownload").checked,
            image_format: document.getElementById("settingsImageFormat").value,
            video_preference: document.getElementById("settingsVideoPreference").value,
            note_format: document.getElementById("settingsNoteFormat").value,
            folder_mode: document.getElementById("settingsFolderMode").checked,
            author_archive: document.getElementById("settingsAuthorArchive").checked,
            download_record: document.getElementById("settingsDownloadRecord").checked,
            record_data: document.getElementById("settingsRecordData").checked,
            write_mtime: document.getElementById("settingsWriteMtime").checked,
            cookie: document.getElementById("settingsCookie").value.trim(),
            user_agent: document.getElementById("settingsUserAgent").value.trim(),
            proxy: document.getElementById("settingsProxy").value.trim() || null,
            timeout: Number(document.getElementById("settingsTimeout").value || 10),
            max_retry: Number(document.getElementById("settingsMaxRetry").value || 5),
            chunk: chunkSize,
            language: document.getElementById("settingsLanguage").value,
            script_server: document.getElementById("settingsScriptServer").checked,
        };
    }

    function renderNativeMonitor(monitor) {
        // 后端状态是监听模式的唯一来源，前端 monitorMode 仅作为交互状态镜像。
        const active = Boolean(monitor.active);
        const wasActive = monitorMode;
        monitorMode = active;
        document.querySelectorAll(".nav-item").forEach((button) => {
            button.disabled = active;
        });
        if (active !== wasActive) setView("monitor", {force: true});
        renderMonitorState(active);
        document.getElementById("monitorCreated").innerHTML = `${monitor.created} <small>${translateText(
            "unit.item")}</small>`;
    }

    function renderNativeAbout(about) {
        // 关于页的版本、发布类型和仓库信息均来自后端常量，避免在 HTML 中固化。
        const version = String(about.version);
        const release = String(about.release);
        document.getElementById("aboutVersion").textContent = [version, release].filter(Boolean).join(" ");
        document.getElementById("aboutAuthor").textContent = about.author;
        document.getElementById("aboutLicense").textContent = about.license;
        document.getElementById("aboutRepository").textContent = String(about.repository).replace(/^https?:\/\//, "");
        aboutLinks = about.links || Object.create(null);
        document.querySelectorAll("[data-about-key]").forEach((button) => {
            const key = button.dataset.aboutKey;
            const link = aboutLinks[key];
            if (!link) return;
            const value = button.querySelector("strong");
            if (value) {
                value.textContent = link.replace(/^https?:\/\//, "");
            }
        });
    }

    function applyNativeState(state) {
        // 应用一次完整状态快照；仅在 revision 变化时重新查询下载记录数据库。
        renderNativeTaskLists(state.tasks, state.files);
        const enabled = Boolean(state.history_enabled);
        const revision = Number(state.history_revision);
        const shouldRefreshHistory = enabled && (lastHistoryRevision !== revision || !historyEnabled);
        setHistoryEnabled(enabled);
        if (shouldRefreshHistory) {
            lastHistoryRevision = revision;
            void requestHistoryPage(historyPage || 1);
        } else if (!enabled) {
            lastHistoryRevision = revision;
        }
        renderNativeLogs(state.logs);
        applyNativeSettings(state.settings);
        renderNativeMonitor(state.monitor);
        renderNativeAbout(state.about);
    }

    async function refreshNativeState() {
        // 轮询期间禁止并发刷新，确保较新的状态快照不会被旧请求覆盖。
        if (bridgeRefreshBusy) return;
        bridgeRefreshBusy = true;
        try {
            applyNativeState(await nativeApi.get_state());
            return true;
        } catch (error) {
            showToast(translateText("update.failed"), "warning");
            return false;
        } finally {
            bridgeRefreshBusy = false;
        }
    }

    async function runNativeAction(action, options = {}) {
        const showLoading = options.loading === true;
        if (showLoading) startupScreen.hidden = false;
        // 写操作完成后立即刷新状态；异常直接显示实际原因，避免误用更新检查提示。
        try {
            await action();
            await refreshNativeState();
        } catch (error) {
            const message = error instanceof Error ? error.message : String(error);
            showToast(message, "warning");
        } finally {
            if (showLoading) startupScreen.hidden = true;
        }
    }

    function startStatePolling() {
        // 用户确认免责声明后才开始轮询完整状态，避免未授权时触发下载器运行时逻辑。
        if (stateRefreshTimer) return;
        stateRefreshTimer = window.setInterval(() => void refreshNativeState(), 500);
    }

    function showDisclaimer() {
        // 免责声明是启动前阻塞确认项，只能通过底部两个按钮继续或退出。
        if (!disclaimerModal.open) disclaimerModal.showModal();
        window.requestAnimationFrame(() => {
            document.getElementById("acceptDisclaimer").focus({preventScroll: true});
        });
    }

    document.getElementById("acceptDisclaimer").addEventListener("click", () => {
        void (async () => {
            try {
                await nativeApi.accept_disclaimer();
                disclaimerModal.close();
                await refreshNativeState();
                startStatePolling();
            } catch (error) {
                const message = error instanceof Error ? error.message : String(error);
                showToast(message, "warning");
            }
        })();
    });

    document.getElementById("declineDisclaimer").addEventListener("click", () => {
        void (async () => {
            try {
                await nativeApi.decline_disclaimer();
            } catch (error) {
                const message = error instanceof Error ? error.message : String(error);
                showToast(message, "warning");
            }
        })();
    });

    // 事件代理统一把桌面端操作转发到 PyWebView API。
    document.addEventListener("click", (event) => {
        const button = event.target.closest("button");
        if (!button) return;
        const id = button.id;
        const taskButton = button.closest("[data-action='cancel']");
        if (taskButton) {
            const taskId = taskButton.closest(".queue-item")?.dataset.taskId;
            if (!taskId) return;
            event.preventDefault();
            event.stopImmediatePropagation();
            void runNativeAction(async () => {
                const cancelled = await nativeApi.cancel_task(taskId);
                if (!cancelled) showToast(
                    translateText("toast.cannot_cancel"), "warning");
            });
            return;
        }
        if (button.dataset.aboutKey) {
            event.preventDefault();
            event.stopImmediatePropagation();
            void runNativeAction(async () => {
                const opened = await nativeApi.open_url(aboutLinks[button.dataset.aboutKey]);
                if (!opened) throw new Error(translateText("toast.browser_unavailable"));
            });
            return;
        }
        if (id === "browseWorkPath") {
            event.preventDefault();
            event.stopImmediatePropagation();
            void runNativeAction(async () => {
                const input = document.getElementById("settingsWorkPath");
                const selected = await nativeApi.browse_directory(input.value);
                if (selected) input.value = selected;
            });
        } else if (id === "confirmDeleteHistory") {
            event.preventDefault();
            event.stopImmediatePropagation();
            void runNativeAction(async () => {
                const ids = selectedHistoryIds();
                if (ids.length === 0) return;
                const result = await nativeApi.delete_history_records(ids, historySearch.value, historyPage);
                recordModal.close();
                renderNativeHistoryPage(result);
                showToast(formatTranslated("history.deleted_selected", [ids.length]));
            });
        } else if (id === "clearFinished") {
            event.preventDefault();
            event.stopImmediatePropagation();
            void runNativeAction(async () => {
                await nativeApi.clear_finished();
            });
        } else if (id === "openDownloadFolder") {
            event.preventDefault();
            event.stopImmediatePropagation();
            void runNativeAction(async () => {
                const opened = await nativeApi.open_download_folder();
                if (!opened) throw new Error(translateText("toast.folder_unavailable"));
            });
        } else if (id === "saveSettings") {
            event.preventDefault();
            event.stopImmediatePropagation();
            void runNativeAction(async () => {
                const result = await nativeApi.save_settings(collectNativeSettings());
                if (!result.ok) throw new Error(result.error);
                settingsLoaded = false;
                await refreshUiTranslations();
                showToast(translateText("settings.saved"));
            }, {loading: true});
        } else if (id === "discardSettings") {
            event.preventDefault();
            event.stopImmediatePropagation();
            void runNativeAction(async () => {
                settingsLoaded = false;
                applyNativeSettings(await nativeApi.get_settings());
                showToast(translateText("settings.discarded"));
            });
        } else if (id === "pageCheckUpdate") {
            event.preventDefault();
            event.stopImmediatePropagation();
            if (pageCheckUpdate.disabled) return;
            setUpdateChecking(true);
            setUpdateResult(translateText("update.checking"), "info");
            void (async () => {
                try {
                    const result = await nativeApi.check_update();
                    if (result.status !== "ok") {
                        setUpdateResult(result.message, "warning");
                        showToast(translateText("update.failed"), "warning");
                        return;
                    }
                    const updateAvailable = ["update_available", "stable_available", "development_current"].includes(
                        result.kind);
                    const tone = updateAvailable ? "warning" : "success";
                    const title = result.title;
                    setUpdateResult(`${title}: ${result.message}`, tone);
                    showToast(title, tone);
                } catch (error) {
                    const message = error?.message || String(error);
                    setUpdateResult(`${translateText("update.failed")}: ${message}`, "error");
                    showToast(translateText("update.failed"), "warning");
                } finally {
                    setUpdateChecking(false);
                }
            })();
        }
    }, true);

    function connectNativeBridge() {
        // pywebviewready 触发后先加载语言包；未同意免责声明时不进入状态轮询。
        nativeApi = window.pywebview.api;
        void (async () => {
            await refreshUiTranslations();
            startupScreen.hidden = true;
            const disclaimer = await nativeApi.get_disclaimer();
            if (!disclaimer.accepted) {
                showDisclaimer();
                return;
            }
            await refreshNativeState();
            startStatePolling();
        })().catch((error) => {
            startupScreen.hidden = true;
            showToast(translateText("toast.language_load_failed"), "warning");
        });
    }

    window.addEventListener("pywebviewready", connectNativeBridge);
})();
