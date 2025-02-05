(function() {
    function fetchStats(pageName) {
        const requestData = {
            page_name: pageName,
            browser: navigator.userAgent,
            screen_width: window.screen.width,
            screen_height: window.screen.height,
            viewport_width: window.innerWidth,
            viewport_height: window.innerHeight,
            referrer: document.referrer,
            language: navigator.language,
            os: navigator.platform,
            timestamp: new Date().toISOString()
        };

        console.log("%cThis page uses an API to track the number of users. 👋\n%cBelow is the data being sent for full transparency:",
            "color: #f8f8f2; background-color: #282a36; font-size: 16px; font-weight: bold; padding: 8px;",
            "color: #50fa7b; font-size: 14px;");

        console.log("%cSent Data:", "color: #ff79c6; font-size: 14px; font-weight: bold;", requestData);

        fetch("https://api.learntogoogle.de/api/counter", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`API request failed with status ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("✅ API Stats Response:", data);

            // Update placeholders with API data
            document.querySelectorAll("[data-placeholder='now']").forEach(el => el.textContent = data.date_stats?.now?.[0] || "-");
            document.querySelectorAll("[data-placeholder='24h']").forEach(el => el.textContent = data.date_stats?.today?.[0] || "-");
            document.querySelectorAll("[data-placeholder='week']").forEach(el => el.textContent = data.date_stats?.week?.[0] || "-");
            document.querySelectorAll("[data-placeholder='month']").forEach(el => el.textContent = data.date_stats?.month?.[0] || "-");
            document.querySelectorAll("[data-placeholder='user_uniq']").forEach(el => el.textContent = data.user_uniq || "-");
        })
        .catch(error => {
            console.error("%c❌ API request failed! Please contact the API administrator.", "color: red; font-size: 14px; font-weight: bold;");
            console.error(error);

            // Set placeholders to "-" if API fails
            document.querySelectorAll("[data-placeholder]").forEach(el => el.textContent = "-");
        });
    }

    document.addEventListener("DOMContentLoaded", function() {
        const scriptTags = document.getElementsByTagName("script");
        for (let script of scriptTags) {
            if (script.src.includes("OpenCounterAPI.js")) {
                let params = script.getAttribute("data-page");
                if (params) {
                    fetchStats(params);
                }
                break;
            }
        }
    });
})();
