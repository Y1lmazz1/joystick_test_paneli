import pygame
import os
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.progress import BarColumn, Progress

console = Console()
def create_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", size=15),
        Layout(name="footer", size=5)
    )
    layout["main"].split_row(
        Layout(name="axes"),
        Layout(name="buttons")
    )
    return layout
def get_joystick_data(j):
    pygame.event.pump()
    

    axes_data = []
    for i in range(j.get_numaxes()):
        val = j.get_axis(i)
        axes_data.append({"id": i, "val": val})
    

    buttons_pressed = [i for i in range(j.get_numbuttons()) if j.get_button(i)]
    

    hat = j.get_hat(0) if j.get_numhats() > 0 else (0, 0)
    
    return axes_data, buttons_pressed, hat

def run_dashboard():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        console.print("[bold red]❌ Hata: Kontrolcü bulunamadı![/bold red]")
        return

    j = pygame.joystick.Joystick(0)
    j.init()

    layout = create_layout()
    
    with Live(layout, refresh_per_second=20, screen=True):
        while True:
            axes, btns, hat = get_joystick_data(j)
            
         
            layout["header"].update(Panel(f"[bold cyan]🎮 Cihaz: {j.get_name()} | Hat: {hat}[/bold cyan]", border_style="blue"))

           
            axes_table = Table(title="🕹️ Analog Eksenleri", expand=True)
            axes_table.add_column("Eksen", justify="center")
            axes_table.add_column("Değer", justify="right")
            axes_table.add_column("Görsel", ratio=1)

            for a in axes:
               
                color = "green" if abs(a['val']) > 0.1 else "white"
                bar_val = (a['val'] + 1) * 50 
                axes_table.add_row(
                    f"Axis {a['id']}", 
                    f"[{color}]{a['val']:>6.2f}[/{color}]",
                    f"[{color}]" + "|" * int(bar_val/2) + "[/]"
                )
            layout["axes"].update(Panel(axes_table, border_style="green"))

           
            btn_text = ", ".join([f"[bold yellow]BT {b}[/]" for b in btns]) if btns else "[grey42]Basılı tuş yok[/]"
            layout["buttons"].update(Panel(f"\n\n{btn_text}", title="🔘 Basılı Butonlar", border_style="yellow"))

       
            footer_text = f"D-PAD: [bold magenta]{hat}[/]  |  Çıkış için [bold red]Ctrl+C[/]"
            layout["footer"].update(Panel(footer_text, border_style="red"))

            time.sleep(0.05)

if __name__ == "__main__":
    try:
        run_dashboard()
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()