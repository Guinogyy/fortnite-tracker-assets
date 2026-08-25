import flet as ft
import flet_audio as fta
import banco_dados
import telas
import ssl
import traceback
import asyncio

ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Fortnite Tracker"
    
    # 🎵 SISTEMA DE SOM DUPLO EM MP3 LOCAL 🎵
    page.bgm_player = fta.Audio(
        src="/login.mp3", 
        autoplay=True, 
        volume=0.4, 
        release_mode=fta.ReleaseMode.LOOP,
        on_loaded=lambda _: print("Rádio BGM carregada!"),
        on_state_change=lambda e: print(f"BGM Estado: {e.state}")
    )
    
    page.preview_player = fta.Audio(
        src="/hud.mp3", 
        autoplay=False, 
        volume=0.7, 
        release_mode=fta.ReleaseMode.STOP,
        on_loaded=lambda _: print("Rádio Preview carregada!"),
        on_state_change=lambda e: print(f"Preview Estado: {e.state}")
    )
    
    page.services.extend([page.bgm_player, page.preview_player])

    # --- SISTEMA DE ROTAS BLINDADO ---
    def mudanca_de_rota(route_event=None):
        try:
            if len(page.views) == 0:
                page.views.append(ft.View(route="/_base", bgcolor=ft.Colors.BLACK))
            
            while len(page.views) > 1:
                page.views.pop()
            
            usuario_logado = banco_dados.ler_sessao()
            banco = banco_dados.carregar_banco()
            avatars = banco_dados.carregar_avatars() or []
            elementais = banco_dados.carregar_elementais() or []
            
            rota = page.route

            if rota == "/":
                rota = "/splash"

            # ==========================================
            # 🎵 LÓGICA DA MÚSICA DE FUNDO
            # ==========================================
            if rota in ["/splash", "/login", "/cadastro"]:
                nova_musica = telas.get_asset("login.mp3")
            else:
                if usuario_logado and usuario_logado in banco:
                    musica_equipada = banco[usuario_logado].get("musica", "hud.mp3")
                    nova_musica = telas.get_asset(musica_equipada)
                else:
                    nova_musica = telas.get_asset("hud.mp3")

            # A SOLUÇÃO DEFINITIVA: Destruir o player antigo e criar um novo
            if page.bgm_player.src != nova_musica:
                
                # 1. Tira o rádio antigo da tomada (mata o som na hora)
                if page.bgm_player in page.services:
                    page.services.remove(page.bgm_player)
                
                # 2. Compra um rádio novo já com a fita certa
                page.bgm_player = fta.Audio(
                    src=nova_musica, 
                    autoplay=True, 
                    volume=0.4, 
                    release_mode=fta.ReleaseMode.LOOP
                )
                
                # 3. Coloca o rádio novo na estante do aplicativo
                page.services.append(page.bgm_player)

            # ==========================================
            # MONTAGEM DAS TELAS
            # ==========================================
            if rota == "/splash":
                page.views.append(telas.criar_view_splash(page))
                page.update()
                
                async def transicao_automatica():
                    await asyncio.sleep(2.0)
                    if usuario_logado:
                        page.navigate("/colecao")
                    else:
                        page.navigate("/login")
                
                page.run_task(transicao_automatica)
                return 
            
            elif rota == "/login":
                page.views.append(telas.criar_view_login(page))
            elif rota == "/cadastro":
                page.views.append(telas.criar_view_cadastro(page, avatars))
            elif rota == "/loja":
                page.views.append(telas.criar_view_loja(page))
            elif rota == "/colecao":
                alvo = page.data if page.data else usuario_logado
                page.views.append(telas.criar_view_colecao(page, usuario_logado, alvo, elementais))
            else:
                page.views.append(telas.criar_view_login(page))

            page.update()

        except Exception as e:
            erro_completo = traceback.format_exc()
            page.views.append(
                ft.View(
                    route="/erro",
                    controls=[
                        ft.SafeArea(
                            content=ft.Column([
                                ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED, size=60),
                                ft.Text("CRASH NO SISTEMA!", color=ft.Colors.RED, size=24, weight=ft.FontWeight.BOLD),
                                ft.Text("Erro técnico detectado:", color=ft.Colors.WHITE),
                                ft.Container(content=ft.Text(erro_completo, color=ft.Colors.RED_200, selectable=True), bgcolor=ft.Colors.BLACK87, padding=15, border_radius=8)
                            ])
                        )
                    ]
                )
            )
            page.update()

    def voltar_view(view_pop_event):
        if len(page.views) > 2:
            page.views.pop()
            page.navigate(page.views[-1].route)

    page.on_route_change = mudanca_de_rota
    page.on_view_pop = voltar_view
    
    mudanca_de_rota()

ft.run(main, assets_dir="assets", route_url_strategy="hash")