/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.html",
        "./ond_eventos/templates/**/*.html",
        "./ond_perfil/templates/**/*.html",
        "./ond_social/templates/**/*.html",
        "./ond_notificacao/templates/**/*.html",
        "./ond_eventos/componentes/*.py",
        "./ond_perfil/componentes/*.py",
        "./ond_social/componentes/*.py",
        "./ond_notificacao/componentes/*.py",
        "./staticfiles/js/ondWebComponents.js",
    ],
    theme: {
        extend: {
            colors: {
                primaria: {
                    light: "#FF8692",
                    DEFAULT: "#FF1044",
                    dark: "#801B25",
                },
                secundaria: {
                    light: "#8248EB",
                    DEFAULT: "#631AE5",
                    dark: "#4A13AC",
                },
                terciaria: {
                    light: "#FFBD4A",
                    DEFAULT: "#FF981D",
                    dark: "#BF8215",
                },
                perigo: {
                    light: "#ff1212",
                    DEFAULT: "#fc0000",
                    dark: "#a30202",
                },
                sucesso: "#2D9E2D",
                complementar: {
                    amarelo: "#FF981D",
                    roxo: "#631AE5",
                },
            },
            fontFamily: {
                primaria: ["Inter", "sans-serif"],
            },
        },
    },
    plugins: [],
};
