(() => {
    "use strict";

    const visible = (element) => {
        if (!element) return false;
        // XHS can retain the QR modal in the DOM after login and hide an
        // ancestor with opacity/aria-hidden. Its box still has dimensions.
        for (let node = element; node; node = node.parentElement) {
            const style = getComputedStyle(node);
            if (node.hidden || node.getAttribute("aria-hidden") === "true"
                || style.display === "none" || style.visibility === "hidden"
                || Number(style.opacity) === 0) return false;
        }
        const rect = element.getBoundingClientRect();
        return rect.width > 0 && rect.height > 0
            && rect.bottom > 0 && rect.right > 0
            && rect.top < innerHeight && rect.left < innerWidth;
    };
    const modal = [...document.querySelectorAll(".login-container")].find(visible);
    const qr = modal && [...modal.querySelectorAll(
        ".qrcode-img, .qrcode img, .qr-code img, img[src^='data:image'], canvas, img",
    )].find((element) => {
        const rect = element.getBoundingClientRect();
        return visible(element) && rect.width >= 120 && Math.abs(rect.width - rect.height) < 24;
    });

    // Keep the original QR node and its refresh handlers; only crop the view.
    if (qr) {
        let crop = window.__xhsDownloaderQrCrop;
        if (!crop || crop.modal !== modal) {
            const content = qr.closest(".container") || modal;
            crop = {
                modal, content, full: false,
                modalStyle: modal.getAttribute("style"),
                contentStyle: content.getAttribute("style"),
            };
            window.__xhsDownloaderQrCrop = crop;
            let toggle = document.getElementById("xhsDownloaderLoginView");
            if (!toggle) {
                toggle = document.createElement("button");
                toggle.id = "xhsDownloaderLoginView";
                toggle.style.cssText = "position:fixed;top:8px;right:8px;z-index:2147483647;padding:7px 12px;border:1px solid #ddd;border-radius:6px;background:#fff;color:#555;cursor:pointer;font-size:12px;";
                document.body.append(toggle);
            }
            toggle.textContent = "显示完整页面";
            toggle.onclick = () => {
                crop.full = !crop.full;
                if (crop.full) {
                    for (const [element, style] of [[modal, crop.modalStyle], [content, crop.contentStyle]]) {
                        if (style === null) element.removeAttribute("style");
                        else element.setAttribute("style", style);
                    }
                }
                toggle.textContent = crop.full ? "仅显示二维码" : "显示完整页面";
            };
        }
        if (!crop.full) {
            const set = (element, rules) => Object.entries(rules).forEach(([name, value]) => (
                element.style.setProperty(name, value, "important")
            ));
            if (crop.content !== modal) {
                set(modal, {position: "fixed", inset: "0", width: "100vw", height: "100vh", transform: "none", background: "#fafafa"});
            }
            set(crop.content, {
                position: "fixed", top: "36px", left: "50%", bottom: "auto", right: "auto",
                transform: "translateX(-50%)", width: "calc(100vw - 32px)", "max-width": "500px",
                "min-height": "0", "max-height": "calc(100vh - 52px)", overflow: "hidden",
                "border-radius": "16px", "box-sizing": "border-box", background: "#fff",
            });
            const height = Math.max(360, qr.getBoundingClientRect().bottom - crop.content.getBoundingClientRect().top + 110);
            set(crop.content, {height: `${Math.ceil(height)}px`});
        }
    }

    // Hydration can turn store fields into Vue refs. Read both plain and
    // reactive values; a stable web_session does not imply login has failed.
    const unwrap = (input) => {
        let value = input;
        for (let depth = 0; depth < 6 && value && typeof value === "object"; depth++) {
            let next = value;
            if (value.__v_isRef && "value" in value) next = value.value;
            else if ("_rawValue" in value) next = value._rawValue;
            else if ("_value" in value) next = value._value;
            if (next === value) break;
            value = next;
        }
        return value;
    };
    const rawUser = window.__INITIAL_STATE__?.user;
    const user = unwrap(rawUser);
    const rawInfo = user?.userInfo;
    const info = unwrap(rawInfo);
    const profile = [...document.querySelectorAll("a[href*='/user/profile/']")].some((element) => (
        visible(element)
        && element.closest(".side-bar, .sidebar, .bottom-nav, .bottom-menu, aside")
        && /^(我|我的|Me|Profile)$/.test(element.textContent.trim())
    ));
    return {
        login_visible: Boolean(modal),
        qr_visible: Boolean(qr),
        authenticated: Boolean(
            unwrap(info?.guest) === false
            || unwrap(user?.loggedIn) === true
            || unwrap(user?.isLogin) === true
            || unwrap(user?.isLoggedIn) === true
            || (!modal && profile)
        ),
        state_shape: !rawUser ? "missing" : rawInfo === info ? "plain" : "ref",
    };
})();
