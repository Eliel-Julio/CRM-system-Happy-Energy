
function footer(){
    const elements = Array.from(document.querySelectorAll('.footer'))

    if (elements.length === 0) return

    const str = '&copy; 2026 <a target="_blank" style="color: #fcde1f;" href="https://happyenergy.com.br/">Happy Energy</a> • Todos os direitos reservados'

    elements.forEach(el => {
        el.innerHTML = str
        el.classList.add('text-center', 'py-3')
    })

    return
}
function loadtheme(){
    
    fetch('/get_configs')
    .then(res => res.json())
    .then(data =>{
        console.log("debug configs carregados", data);
        const theme = data.user.theme || 'light'
        console.log("debug theme carregado", theme);
        document.documentElement.setAttribute('data-bs-theme', theme)
    })
}

function definitions(){
    footer()
    loadtheme()
}
const body = document.querySelector('body')
body.onload = definitions