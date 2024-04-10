/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./templates/*", "./templates/languages/*"],
    theme: {
        extend: {
            fontFamily: {
                "poppins": ['"Poppins"', "sans"]
            },
            colors: {
                "accent": "#2CB57E",
            },
            screens: {
                "dashboard-resize": "1080px",
                "resize": "265px"
            }
        },
    },

    plugins: [],
}

// npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch