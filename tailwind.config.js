/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./build/**/*.{html,js}"],
    theme: {
        extend: {
            colors: {
                'cgreen': {
                    300: "#00bc00",
                    500: "#006300",
                }
            }
        }
    }
}
