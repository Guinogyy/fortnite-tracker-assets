import flet as ft
import math

def main(page: ft.Page):
    page.title = "HUD Comando Central"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Estado reativo simples para alternar o modo de sistema
    system_status = ft.Text("SISTEMA ONLINE", color=ft.Colors.GREEN_ACCENT, weight=ft.FontWeight.BOLD, size=16)
    core_glow = ft.Container(
        width=120,
        height=120,
        border_radius=60,
        bgcolor=ft.Colors.CYAN_900,
        animate=ft.Animation(800, ft.AnimationCurve.EASE_OUT_CUBIC),
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(ft.Icons.SECURITY, size=40, color=ft.Colors.CYAN_ACCENT)
    )

    def toggle_shield(e):
        if core_glow.bgcolor == ft.Colors.CYAN_900:
            core_glow.bgcolor = ft.Colors.RED_900
            core_glow.content.name = ft.Icons.WARNING_ROUNDED
            core_glow.content.color = ft.Colors.RED_ACCENT
            system_status.value = "ALERTA DE SEGURANÇA: ESCUDOS ATIVOS"
            system_status.color = ft.Colors.RED_ACCENT
        else:
            core_glow.bgcolor = ft.Colors.CYAN_900
            core_glow.content.name = ft.Icons.SECURITY
            core_glow.content.color = ft.Colors.CYAN_ACCENT
            system_status.value = "SISTEMA ONLINE"
            system_status.color = ft.Colors.GREEN_ACCENT
        page.update()

    # Montando a interface central em Stack com Cards decorativos
    hud_panel = ft.Container(
        width=500,
        height=400,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=["#0f172a", "#1e1b4b"]
        ),
        border=ft.Border.all(2, ft.Colors.CYAN_800),
        border_radius=20,
        padding=20,
        content=ft.Stack(
            controls=[
                # Cabeçalho do HUD
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("DIAGNÓSTICO DO NÚCLEO", color=ft.Colors.CYAN_200, weight=ft.FontWeight.BOLD),
                        system_status
                    ]
                ),
                # Elemento Central Animado
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        controls=[
                            core_glow,
                            ft.Button(
                                content="INVERTER ESTADO DO NÚCLEO",
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.INDIGO_700,
                                    shape=ft.RoundedRectangleBorder(radius=8)
                                ),
                                on_click=toggle_shield
                            )
                        ]
                    )
                ),
                # Rodapé decorativo com métricas simuladas
                ft.Container(
                    bottom=0,
                    left=0,
                    right=0,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.Text("CPU: 14.2%", color=ft.Colors.GREY_400, size=12),
                            ft.Text("MEM: 42.8GB", color=ft.Colors.GREY_400, size=12),
                            ft.Text("LATÊNCIA: 12ms", color=ft.Colors.GREY_400, size=12),
                        ]
                    )
                )
            ]
        )
    )

    page.add(
        ft.SafeArea(
            content=hud_panel
        )
    )

if __name__ == "__main__":
    ft.run(main)