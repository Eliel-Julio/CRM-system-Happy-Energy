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
function navbar(){
    const elements = Array.from(document.querySelectorAll('.navbar'))

    if (elements.length === 0) return
    elements.forEach(el => {
        el.classList.add('navbar', 'navbar-expand-lg', 'shadow-sm', 'sticky-top')
        const urls = el.innerHTML.split(';')
        el.innerHTML =`
        <div class="container-fluid">
            <a class="navbar-brand" href="${urls[0]}">
                <i class="bi bi-lightning-fill"></i> Happy Energy
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="${urls[1]}"><i class="bi bi-box"></i> Configurações</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" href="${urls[2]}"><i class="bi bi-box"></i> Kits</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="${urls[3]}"><i class="bi bi-people"></i> Leads</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="${urls[4]}"><i class="bi bi-file-earmark-text"></i> Propostas</a>
                    </li>
                </ul>
            </div>
        </div>`
    })
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
    navbar()
}
const body = document.querySelector('body')
body.onload = definitions