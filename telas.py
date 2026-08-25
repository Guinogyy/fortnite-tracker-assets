import flet as ft
import flet_video as ftv
import banco_dados
import asyncio
import os

def get_asset(caminho):
    if not caminho:
        return ""
    if str(caminho).startswith(("http", "/")):
        return caminho
        
    caminho = caminho.replace("assets/", "").replace("assets\\", "").lstrip("/")
    
    # MÚSICAS, CAPAS E VÍDEOS: Lidos direto da pasta local 'assets'
    if caminho.endswith(".mp3") or caminho.endswith(".mp4") or caminho.startswith("capa_") or caminho == "vbucks.png":
        return f"/{caminho}"
        
    # IMAGENS GERAIS: Continuam vindo da nuvem
    link_base_github = "https://raw.githubusercontent.com/Guinogyy/fortnite-tracker-assets/main/"
    return f"{link_base_github}{caminho}?v=nova_temporada"

fundo_imagem = ft.DecorationImage(src="https://raw.githubusercontent.com/Guinogyy/fortnite-tracker-assets/refs/heads/main/Gemini_Generated_Image_p89qaip89qaip89q.jpg", fit=ft.BoxFit.COVER)
fundo_azul_clean = ft.RadialGradient(center=ft.alignment.Alignment(0, 0), radius=1.5, colors=["#1a78c2", "#08305c"])
fundo_fortnite = ft.LinearGradient(begin=ft.alignment.Alignment(0, -1), end=ft.alignment.Alignment(0, 1), colors=["#1a4b8c", "#0b2545"])

def animar_hover(e):
    e.control.scale = 1.05 if e.data == "true" else 1.0
    e.control.update()

# =======================================================
# VIEW 0 & 1 & 2: SPLASH, LOGIN, CADASTRO 
# =======================================================
def criar_view_splash(page: ft.Page):
    return ft.View(route="/splash", padding=0, controls=[
        ft.Container(
            expand=True, image=fundo_imagem, 
            content=ft.Container(
                expand=True, bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK), 
                content=ft.Column([
                    ft.ProgressRing(color="#f3d738", stroke_width=4), 
                    ft.Container(height=10), 
                    ft.Text("CONECTANDO AOS SERVIDORES...", weight=ft.FontWeight.W_900, color=ft.Colors.WHITE, size=14, style=ft.TextStyle(letter_spacing=2))
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        )
    ])

def criar_view_login(page: ft.Page):
    input_nome = ft.TextField(label="Nome de Usuário", width=320, border_radius=4, filled=True, bgcolor=ft.Colors.WHITE, border_color=ft.Colors.TRANSPARENT, color=ft.Colors.BLACK, label_style=ft.TextStyle(color=ft.Colors.BLACK54))
    input_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=320, border_radius=4, filled=True, bgcolor=ft.Colors.WHITE, border_color=ft.Colors.TRANSPARENT, color=ft.Colors.BLACK, label_style=ft.TextStyle(color=ft.Colors.BLACK54))
    lbl_erro = ft.Text("", color=ft.Colors.RED_300, size=13, weight=ft.FontWeight.BOLD)
    container_acao = ft.Container(width=320, alignment=ft.alignment.Alignment(0, 0))

    async def tentar_login(e):
        lbl_erro.value = ""
        nome_digitado = input_nome.value.strip() 
        senha_digitada = input_senha.value.strip()
        if not nome_digitado or not senha_digitada:
            lbl_erro.value = "⚠️ Preencha usuário e senha."
            page.update()
            return
        banco = banco_dados.carregar_banco()
        if nome_digitado not in banco:
            lbl_erro.value = "❌ Usuário não existe. Crie uma conta!"
            page.update()
            return
        if banco[nome_digitado].get("senha", "") != senha_digitada:
            lbl_erro.value = "❌ Senha incorreta!"
            page.update()
            return

        original = container_acao.content
        container_acao.content = ft.ProgressRing(color=ft.Colors.WHITE)
        page.update()
        await asyncio.sleep(0.5)
        banco_dados.salvar_sessao(nome_digitado)
        page.data = nome_digitado 
        page.navigate("/colecao")

    btn_entrar = ft.Button(content=ft.Text("RELAUNCH", weight=ft.FontWeight.W_900, size=16), style=ft.ButtonStyle(bgcolor="#f3d738", color=ft.Colors.BLACK, shape=ft.RoundedRectangleBorder(radius=4), padding=20), width=320, on_click=tentar_login)
    input_nome.on_submit = tentar_login
    input_senha.on_submit = tentar_login
    container_acao.content = btn_entrar

    return ft.View(route="/login", padding=0, controls=[
        ft.Container(
            expand=True, gradient=fundo_azul_clean, 
            content=ft.Container(expand=True, alignment=ft.alignment.Alignment(0, 0), content=ft.Column([
                ft.Text("FORTNITE", size=60, weight=ft.FontWeight.W_900, color=ft.Colors.WHITE, style=ft.TextStyle(letter_spacing=-2)), 
                ft.Text("LOGIN REQUIRED", size=16, weight=ft.FontWeight.BOLD, color="#f3d738"), 
                ft.Container(height=20), 
                input_nome, input_senha, lbl_erro, 
                ft.Container(height=10), container_acao, 
                ft.Container(height=15), 
                ft.Text("New here? Please create an account below.", color=ft.Colors.WHITE54, size=12), 
                ft.TextButton("CRIAR NOVA CONTA", on_click=lambda _: page.navigate("/cadastro"), style=ft.ButtonStyle(color=ft.Colors.WHITE))
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, tight=True, spacing=5))
        )
    ])

def criar_view_cadastro(page: ft.Page, lista_avatars):
    input_nome = ft.TextField(label="Escolha um Usuário", width=320, border_radius=4, filled=True, bgcolor=ft.Colors.WHITE, border_color=ft.Colors.TRANSPARENT, color=ft.Colors.BLACK, label_style=ft.TextStyle(color=ft.Colors.BLACK54))
    input_senha = ft.TextField(label="Crie uma Senha", password=True, can_reveal_password=True, width=320, border_radius=4, filled=True, bgcolor=ft.Colors.WHITE, border_color=ft.Colors.TRANSPARENT, color=ft.Colors.BLACK, label_style=ft.TextStyle(color=ft.Colors.BLACK54))
    lbl_erro = ft.Text("", color=ft.Colors.RED_300, size=13, weight=ft.FontWeight.BOLD)
    
    # Garante que lista_avatars lide tanto com dicts (novo formato) quanto strings (formato antigo)
    def get_arq_avatar(item):
        return item["arquivo"] if isinstance(item, dict) else item

    avatar_selecionado = get_arq_avatar(lista_avatars[0]) if lista_avatars else ""
    avatar_containers = []

    def selecionar_avatar(arq, container_clicado):
        nonlocal avatar_selecionado
        avatar_selecionado = arq
        for c in avatar_containers:
            c.bgcolor = ft.Colors.TRANSPARENT
            c.border = ft.Border.all(2, ft.Colors.with_opacity(0.3, ft.Colors.WHITE))
            c.update()
        container_clicado.bgcolor = ft.Colors.with_opacity(0.3, ft.Colors.WHITE)
        container_clicado.border = ft.Border.all(3, ft.Colors.WHITE)
        container_clicado.update()

    linha_avatars = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER, 
        spacing=10,
        wrap=True,      # <-- Faz as fotos descerem para a linha de baixo se faltar espaço
        run_spacing=10, # <-- Adiciona um espaçamento vertical entre as fileiras
        width=320       # <-- Trava a largura para ficar idêntica à caixa de "Nome de Usuário"
    )
    for item in lista_avatars:
        arq = get_arq_avatar(item)
        is_selected = (arq == avatar_selecionado)
        c_avatar = ft.Container(content=ft.Image(src=get_asset(arq), width=45, height=45, fit=ft.BoxFit.CONTAIN), bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.WHITE) if is_selected else ft.Colors.TRANSPARENT, border=ft.Border.all(3, ft.Colors.WHITE) if is_selected else ft.Border.all(2, ft.Colors.with_opacity(0.3, ft.Colors.WHITE)), padding=5, border_radius=12, ink=True, scale=1.0, animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT), on_hover=animar_hover)
        c_avatar.on_click = lambda e, a=arq, c=c_avatar: selecionar_avatar(a, c)
        avatar_containers.append(c_avatar)
        linha_avatars.controls.append(c_avatar)

    async def registrar_conta(e):
        lbl_erro.value = ""
        nome_digitado = input_nome.value.strip()
        senha_digitada = input_senha.value.strip()
        if not nome_digitado or not senha_digitada:
            lbl_erro.value = "⚠️ Preencha todos os campos."
            page.update()
            return
        banco = banco_dados.carregar_banco()
        if nome_digitado in banco:
            lbl_erro.value = "⚠️ Nome já em uso. Tente outro!"
            page.update()
            return
        
        banco[nome_digitado] = {"senha": senha_digitada, "avatar": avatar_selecionado, "musica": "hud.mp3", "vbucks": 0, "avatares_comprados": [avatar_selecionado] if avatar_selecionado else [], "musicas_compradas": ["hud.mp3"], "colecao": {}}
        banco_dados.salvar_banco(banco)
        banco_dados.salvar_sessao(nome_digitado)
        page.data = nome_digitado
        page.navigate("/colecao")

    input_nome.on_submit = registrar_conta
    input_senha.on_submit = registrar_conta

    return ft.View(route="/cadastro", padding=0, controls=[
        ft.Container(expand=True, gradient=fundo_azul_clean, content=ft.Container(expand=True, alignment=ft.alignment.Alignment(0, 0), content=ft.Column([ft.Text("NEW RECRUIT", size=30, weight=ft.FontWeight.W_900, color=ft.Colors.WHITE), ft.Container(height=10), ft.Text("ESCOLHA SEU AVATAR INICIAL:", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE54), linha_avatars, ft.Container(height=15), input_nome, input_senha, lbl_erro, ft.Button("CONFIRMAR CADASTRO", style=ft.ButtonStyle(bgcolor="#f3d738", color=ft.Colors.BLACK, shape=ft.RoundedRectangleBorder(radius=4), padding=20), width=320, on_click=registrar_conta), ft.TextButton("Voltar para o Login", on_click=lambda _: page.navigate("/login"), style=ft.ButtonStyle(color=ft.Colors.WHITE))], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, tight=True, spacing=10)))
    ])

# =======================================================
# VIEW 3: TELA DE COLEÇÃO
# =======================================================
def criar_view_colecao(page: ft.Page, usuario_logado, usuario_alvo, dados_elementais):
    banco = banco_dados.carregar_banco()
    dados_alvo = banco.get(usuario_alvo, {"avatar": "", "vbucks": 0, "colecao": {}})
    progresso_user = dados_alvo.get("colecao", {})
    carteira_vbucks = dados_alvo.get("vbucks", 0)
    avatar_atual = dados_alvo.get("avatar", "")
    eh_meu_perfil = (usuario_logado == usuario_alvo)
    total_elementais = len(dados_elementais)
    pegos_count = sum(1 for v in progresso_user.values() if isinstance(v, dict) and v.get("pegou"))
    texto_saudacao = f"Operador: {usuario_logado.upper()}" if eh_meu_perfil else f"Inspecionando: {usuario_alvo.upper()}"

    def recarregar_tela(novo_alvo=None):
        if novo_alvo: page.data = novo_alvo
        alvo = page.data if page.data else usuario_logado
        page.views.pop()
        page.views.append(criar_view_colecao(page, usuario_logado, alvo, dados_elementais))
        page.update()

    def efetuar_logout(e):
        try:
            if os.path.exists("sessao_login.txt"): os.remove("sessao_login.txt")
        except: pass
        page.data = None
        
        async def calar_preview():
            try: await page.preview_player.pause()
            except: pass
        page.run_task(calar_preview)
        
        page.navigate("/login")

    def abrir_troca_avatar(e):
        if not eh_meu_perfil: return
        comprados = dados_alvo.get("avatares_comprados", [])
        if not comprados: return
        def escolher(arq):
            banco[usuario_logado]["avatar"] = arq
            banco_dados.salvar_banco(banco)
            page.pop_dialog()
            recarregar_tela()
        grade_imgs = ft.Row(wrap=True, spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        for arq in comprados:
            b_img = ft.Container(content=ft.Image(src=get_asset(arq), width=50, height=50, fit=ft.BoxFit.CONTAIN), bgcolor=ft.Colors.BLACK54, border_radius=10, padding=5, ink=True, border=ft.Border.all(2, ft.Colors.CYAN_ACCENT) if arq == avatar_atual else None, on_click=lambda _, a=arq: escolher(a))
            grade_imgs.controls.append(b_img)
        page.show_dialog(ft.AlertDialog(title=ft.Text("Escolha seu novo Avatar"), content=ft.Container(content=grade_imgs, width=300, height=150), actions=[ft.TextButton("Fechar", on_click=lambda _: page.pop_dialog())]))

    container_avatar = ft.Container(content=ft.Image(src=get_asset(avatar_atual), width=45, height=45, fit=ft.BoxFit.CONTAIN) if avatar_atual else ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK45, border_radius=22.5, width=45, height=45, alignment=ft.alignment.Alignment(0, 0), border=ft.Border.all(2, "#f3d738"), ink=eh_meu_perfil, on_click=abrir_troca_avatar if eh_meu_perfil else None, tooltip="Clique para alterar seu avatar" if eh_meu_perfil else None)

    hud_topo = ft.Row([container_avatar, ft.Text(texto_saudacao, size=20, weight=ft.FontWeight.W_900, color="#f3d738"), ft.Container(expand=True), ft.Container(content=ft.Row([ft.Image(src=get_asset("vbucks.png"), width=20, height=20), ft.Text(f"{carteira_vbucks}", weight=ft.FontWeight.BOLD)]), bgcolor=ft.Colors.BLACK54, padding=8, border_radius=10), ft.ElevatedButton("LOJA", icon=ft.Icons.STORE, color=ft.Colors.BLACK, bgcolor="#f3d738", on_click=lambda _: page.navigate("/loja")) if eh_meu_perfil else ft.Container(), ft.IconButton(ft.Icons.LOGOUT, tooltip="Sair", icon_color=ft.Colors.RED_300, on_click=efetuar_logout) if eh_meu_perfil else ft.Container()], alignment=ft.MainAxisAlignment.START)

    grid_geral = ft.GridView(expand=1, runs_count=5, max_extent=110, child_aspect_ratio=0.7, spacing=15, run_spacing=15)

    def ciclar_status(nome_elemental):
        if not eh_meu_perfil: return
        if nome_elemental not in progresso_user or isinstance(progresso_user[nome_elemental], bool): progresso_user[nome_elemental] = {"pegou": False, "dominou": False}
        status = progresso_user[nome_elemental]
        vb = banco[usuario_logado].get("vbucks", 0)
        if status["dominou"]:
            progresso_user[nome_elemental] = {"pegou": False, "dominou": False}
            vb = max(0, vb - 10)
        elif status["pegou"]:
            progresso_user[nome_elemental] = {"pegou": True, "dominou": True}
            vb += 10
        else:
            progresso_user[nome_elemental] = {"pegou": True, "dominou": False}
        banco[usuario_logado]["vbucks"] = vb
        banco[usuario_logado]["colecao"] = progresso_user
        banco_dados.salvar_banco(banco)
        recarregar_tela()

    for item in dados_elementais:
        nome_elem = item["nome"]
        status = progresso_user.get(nome_elem, {"pegou": False, "dominou": False})
        cor_fundo, cor_texto, texto_btn = "#222222", ft.Colors.WHITE54, "Falta"
        if status.get("dominou", False): cor_fundo, cor_texto, texto_btn = "#f3d738", ft.Colors.BLACK, "👑 Dominou"
        elif status.get("pegou", False): cor_fundo, cor_texto, texto_btn = "#0052cc", ft.Colors.WHITE, "✅ Pegou"
        grid_geral.controls.append(ft.Container(content=ft.Column([ft.Image(src=get_asset(item["arquivo"]), width=55, height=55, fit=ft.BoxFit.CONTAIN), ft.Container(content=ft.Text(texto_btn, color=cor_texto, weight=ft.FontWeight.BOLD, size=11), bgcolor=cor_fundo, padding=6, border_radius=4)], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK), border_radius=12, padding=10, ink=eh_meu_perfil, border=ft.Border.all(1, ft.Colors.WHITE24), scale=1.0, animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT), on_hover=animar_hover, on_click=lambda e, n=nome_elem: ciclar_status(n)))

    lista_jogadores = [nome for nome in banco.keys() if nome != usuario_logado]
    botoes_amigos = []
    for nome in lista_jogadores:
        p_amigo = banco[nome].get("colecao", {})
        a_amigo = banco[nome].get("avatar", "")
        pegos = sum(1 for v in p_amigo.values() if isinstance(v, dict) and v.get("pegou"))
        progresso_perc = pegos / total_elementais if total_elementais > 0 else 0
        botoes_amigos.append(ft.Container(content=ft.Column([ft.Row([ft.Image(src=get_asset(a_amigo), width=25, height=25, fit=ft.BoxFit.CONTAIN) if a_amigo else ft.Icon(ft.Icons.PERSON, size=20), ft.Text(nome.upper(), weight=ft.FontWeight.BOLD, size=12)]), ft.ProgressBar(value=progresso_perc, color="#f3d738", bgcolor=ft.Colors.WHITE24, height=6)], spacing=5), bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK), padding=10, border_radius=10, ink=True, width=150, border=ft.Border.all(1, ft.Colors.CYAN_800 if nome == usuario_alvo else ft.Colors.TRANSPARENT), scale=1.0, animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT), on_hover=animar_hover, on_click=lambda e, n=nome: recarregar_tela(n)))

    linha_amigos = ft.Column([ft.Text("ESQUADRÃO DO LOBBY", size=11, weight=ft.FontWeight.W_900, color=ft.Colors.CYAN_ACCENT), ft.Row(botoes_amigos, scroll=ft.ScrollMode.AUTO)], spacing=5) if botoes_amigos else ft.Container()

    return ft.View(route="/colecao", padding=0, controls=[
        ft.Container(expand=True, image=fundo_imagem, gradient=fundo_fortnite, content=ft.Container(expand=True, bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK), padding=20, content=ft.Column([hud_topo, ft.Divider(color="white24"), ft.Row([ft.Text(f"PROGRESSO DE COLEÇÃO: {pegos_count}/{total_elementais}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), ft.ProgressBar(value=pegos_count/total_elementais if total_elementais>0 else 0, color="#f3d738", expand=True)]), grid_geral, linha_amigos, ft.TextButton("← Voltar para meu perfil", icon=ft.Icons.ARROW_BACK, style=ft.ButtonStyle(color=ft.Colors.WHITE), on_click=lambda _: recarregar_tela(usuario_logado)) if not eh_meu_perfil else ft.Container()], horizontal_alignment=ft.CrossAxisAlignment.STRETCH)))
    ])

# =======================================================
# VIEW 4: TELA DA LOJA
# =======================================================
def criar_view_loja(page: ft.Page):
    usuario_logado = banco_dados.ler_sessao()
    banco = banco_dados.carregar_banco()
    
    itens_avatars = banco_dados.carregar_loja_avatars()
    itens_musicas = banco_dados.carregar_loja_musicas()

    dados_user = banco.get(usuario_logado, {})
    vbucks = dados_user.get("vbucks", 0)
    
    avatar_atual = dados_user.get("avatar", "")
    musica_atual = dados_user.get("musica", "hud.mp3")
    
    avatares_comprados = dados_user.get("avatares_comprados", [avatar_atual] if avatar_atual else [])
    musicas_compradas = dados_user.get("musicas_compradas", ["hud.mp3"])

    lbl_mensagem = ft.Text("", color=ft.Colors.RED_ACCENT, weight=ft.FontWeight.BOLD)
    grid_avatars = ft.Row(wrap=True, spacing=15, run_spacing=15, alignment=ft.MainAxisAlignment.START)
    grid_musicas = ft.Row(wrap=True, spacing=15, run_spacing=15, alignment=ft.MainAxisAlignment.START)

    def recarregar_loja():
        page.views.pop()
        page.views.append(criar_view_loja(page))
        page.update()

    def comprar_avatar(item):
        arq = item["arquivo"]
        if arq in avatares_comprados:
            banco[usuario_logado]["avatar"] = arq
            banco_dados.salvar_banco(banco)
            recarregar_loja()
        else:
            if vbucks >= item["preco"]:
                banco[usuario_logado]["vbucks"] -= item["preco"]
                banco[usuario_logado]["avatares_comprados"].append(arq)
                banco[usuario_logado]["avatar"] = arq
                banco_dados.salvar_banco(banco)
                recarregar_loja()
            else:
                lbl_mensagem.value = "❌ V-Bucks insuficientes para o Avatar!"
                page.update()

    def comprar_musica(item):
        arq = item["arquivo"]
        if arq in musicas_compradas:
            banco[usuario_logado]["musica"] = arq
            banco_dados.salvar_banco(banco)
            page.bgm_player.src = get_asset(arq)
            page.bgm_player.update()
            
            async def run_play():
                try: await page.bgm_player.play()
                except: pass
            page.run_task(run_play)
            
            recarregar_loja()
        else:
            if vbucks >= item["preco"]:
                banco[usuario_logado]["vbucks"] -= item["preco"]
                banco[usuario_logado]["musicas_compradas"].append(arq)
                banco[usuario_logado]["musica"] = arq
                banco_dados.salvar_banco(banco)
                page.bgm_player.src = get_asset(arq)
                page.bgm_player.update()
                
                async def run_play():
                    try: await page.bgm_player.play()
                    except: pass
                page.run_task(run_play)
                
                recarregar_loja()
            else:
                lbl_mensagem.value = "❌ V-Bucks insuficientes para a Música!"
                page.update()

    def criar_handler_tocar(arq):
        async def tocar_preview(e):
            try: 
                await page.bgm_player.pause() 
            except Exception as err: 
                print(f"Erro ao pausar BGM: {err}")
            
            page.preview_player.src = get_asset(arq)
            page.preview_player.update()
            
            try: 
                await page.preview_player.play() 
            except Exception as err: 
                print(f"Erro ao tocar Preview: {err}")
        return tocar_preview

    async def parar_preview(e):
        try: 
            await page.preview_player.pause()
        except Exception as err: 
            print(f"Erro ao pausar Preview: {err}")
        try: 
            await page.bgm_player.resume()
        except Exception as err: 
            print(f"Erro ao resumir BGM: {err}")

    async def voltar_para_colecao(e):
        await parar_preview(e)
        page.navigate("/colecao")

    # Cores de Raridade para Avatares
    # Cores de Raridade para Avatares
    cores_raridade = {
        "comum": "#707070",   # Cinza
        "incomum": "#319236", # Verde
        "raro": "#4c51f7",    # Azul
        "epico": "#9d4dbb",   # Roxo
        "lendario": "#f3af19" # Dourado
    }

    # Gradientes de fundo para brilhar por trás do PNG transparente
    fundos_raridade = {
        "comum": ft.LinearGradient(begin=ft.alignment.Alignment(0, -1), end=ft.alignment.Alignment(0, 1), colors=["#8a8a8a", "#3b3b3b"]),
        "incomum": ft.LinearGradient(begin=ft.alignment.Alignment(0, -1), end=ft.alignment.Alignment(0, 1), colors=["#40c147", "#174719"]),
        "raro": ft.LinearGradient(begin=ft.alignment.Alignment(0, -1), end=ft.alignment.Alignment(0, 1), colors=["#5e64ff", "#1b1d5c"]),
        "epico": ft.LinearGradient(begin=ft.alignment.Alignment(0, -1), end=ft.alignment.Alignment(0, 1), colors=["#bd5ce0", "#3d1e49"]),
        "lendario": ft.LinearGradient(begin=ft.alignment.Alignment(0, -1), end=ft.alignment.Alignment(0, 1), colors=["#ffba26", "#735108"])
    }

    # ==================================
    # AVATARES ESTILIZADOS
    # ==================================
    for item in itens_avatars:
        arq = item["arquivo"]
        nome_skin = item.get("nome", "Desconhecido")
        raridade = item.get("raridade", "incomum")
        tag = item.get("tag", "")
        
        cor_borda = cores_raridade.get(raridade, "#707070")
        gradiente_fundo = fundos_raridade.get(raridade, fundos_raridade["comum"])
        
        eh_o_atual = (arq == avatar_atual)
        if eh_o_atual: txt_btn, bg_btn = "Usando", "#4b5563"
        elif arq in avatares_comprados: txt_btn, bg_btn = "Equipar", "#0052cc"
        else: txt_btn, bg_btn = f"Comprar ({item['preco']})", "#f3d738"
        cor_txt = ft.Colors.BLACK if bg_btn=="#f3d738" else ft.Colors.WHITE

        # Cria a tag do esquadrão se ela existir
        selo_ui = ft.Container(
            content=ft.Text(tag.upper(), size=9, weight=ft.FontWeight.W_900, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED_700,
            padding=4,
            border_radius=4
        ) if tag else ft.Container()

        grid_avatars.controls.append(ft.Container(
            width=120,
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
            border_radius=8,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            border=ft.Border.all(3, ft.Colors.WHITE) if eh_o_atual else ft.Border.all(2, cor_borda),
            scale=1.0, animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT), on_hover=animar_hover,
            content=ft.Column(
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # A MÁGICA ACONTECE AQUI: O Container pinta o fundo e a Imagem fica por cima
                    ft.Stack([
                        ft.Container(
                            width=120, height=120,
                            gradient=gradiente_fundo,
                            content=ft.Image(src=get_asset(arq), fit=ft.BoxFit.CONTAIN)
                        ),
                        ft.Container(content=selo_ui, alignment=ft.alignment.Alignment(0, -1), padding=5)
                    ]),
                    # Faixa de cor da raridade
                    ft.Container(
                        bgcolor=cor_borda,
                        width=120, padding=2, alignment=ft.alignment.Alignment(0, 0),
                        content=ft.Text(nome_skin.upper(), size=10, weight=ft.FontWeight.W_900, color=ft.Colors.WHITE, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS)
                    ),
                    # Botão de Ação
                    ft.Container(
                        padding=8, alignment=ft.alignment.Alignment(0, 0),
                        content=ft.Container(
                            content=ft.Text(txt_btn, color=cor_txt, weight=ft.FontWeight.BOLD, size=11), 
                            bgcolor=bg_btn, padding=6, border_radius=4, ink=True, alignment=ft.alignment.Alignment(0, 0),
                            on_click=lambda e, it=item: comprar_avatar(it)
                        )
                    )
                ]
            )
        ))

    # ==================================
    # MÚSICAS COM CAPAS EM VÍDEO
    # ==================================
    for item in itens_musicas:
        arq = item["arquivo"]
        capa = item.get("capa", "")
        eh_o_atual = (arq == musica_atual)
        
        if eh_o_atual: txt_btn, bg_btn = "Equipada", "#4b5563"
        elif arq in musicas_compradas: txt_btn, bg_btn = "Equipar", "#0052cc"
        else: txt_btn, bg_btn = f"Comprar ({item['preco']})", "#f3d738"
        cor_txt = ft.Colors.BLACK if bg_btn=="#f3d738" else ft.Colors.WHITE

        if capa.endswith(".mp4"):
            midia_capa = ftv.Video(
                playlist=[ftv.VideoMedia(get_asset(capa))],
                autoplay=True,
                muted=True,
                volume=0.0,
                controls=None,
                width=160,
                height=130,
                fit=ft.BoxFit.COVER,
                playlist_mode=ftv.PlaylistMode.LOOP
            )
        else:
            midia_capa = ft.Image(src=get_asset(capa), width=160, height=130, fit=ft.BoxFit.COVER)

        card_musica = ft.Container(
            width=160,
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
            border_radius=12,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            border=ft.Border.all(2, ft.Colors.WHITE) if eh_o_atual else ft.Border.all(1, ft.Colors.WHITE24),
            scale=1.0, animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT), on_hover=animar_hover,
            content=ft.Column(
                spacing=0,
                controls=[
                    midia_capa,
                    ft.Container(
                        padding=10,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=6,
                            controls=[
                                ft.Text(item["nome"], size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Row([
                                    ft.IconButton(ft.Icons.PLAY_ARROW, icon_color=ft.Colors.YELLOW, on_click=criar_handler_tocar(arq), tooltip="Ouvir Preview"),
                                    ft.IconButton(ft.Icons.STOP, icon_color=ft.Colors.YELLOW, on_click=parar_preview, tooltip="Parar Preview")
                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=0),
                                ft.Container(
                                    content=ft.Text(txt_btn, color=cor_txt, weight=ft.FontWeight.BOLD, size=11), 
                                    bgcolor=bg_btn, padding=6, border_radius=4, ink=True, 
                                    alignment=ft.alignment.Alignment(0, 0),
                                    on_click=lambda e, it=item: comprar_musica(it)
                                )
                            ]
                        )
                    )
                ]
            )
        )
        grid_musicas.controls.append(card_musica)

    return ft.View(route="/loja", padding=0, controls=[
        ft.Container(
            expand=True, image=fundo_imagem, gradient=fundo_fortnite,
            content=ft.Container(
                expand=True, bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK), padding=20,
                content=ft.Column([
                    ft.Row([
                        ft.IconButton(ft.Icons.ARROW_BACK, icon_color=ft.Colors.WHITE, on_click=voltar_para_colecao),
                        ft.Text("LOJA DE ITENS", size=24, weight=ft.FontWeight.W_900, color="#f3d738"),
                        ft.Container(expand=True),
                        ft.Row([ft.Image(src=get_asset("vbucks.png"), width=24, height=24), ft.Text(f"{vbucks} V-Bucks", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)])
                    ]),
                    lbl_mensagem,
                    ft.Divider(color="white24"),
                    ft.Column([
                        ft.Text("FOTOS DE PERFIL", size=16, weight=ft.FontWeight.W_900, color=ft.Colors.CYAN_ACCENT),
                        grid_avatars,
                        ft.Container(height=10),
                        ft.Text("MÚSICAS (PACOTES DE MÚSICA DO LOBBY)", size=16, weight=ft.FontWeight.W_900, color=ft.Colors.CYAN_ACCENT),
                        grid_musicas
                    ], scroll=ft.ScrollMode.AUTO, expand=True)
                ])
            )
        )
    ])