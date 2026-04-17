import flet as ft
import datetime
import random

def main(page: ft.Page):
    # Configuración principal de la página
    page.title = "The Tortured Poets Department: Academic Edition"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.spacing = 20
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.window_width = 450
    page.window_height = 800

    # ------------------ DATOS Y LÓGICA ------------------
    
    eras_config = {
        "Lover": {"color": "#FFB6C1", "bg_grad": ["#ffe6ea", "#ffb6c1"], "diff": "Easy"},
        "Red": {"color": "#8B0000", "bg_grad": ["#ff4d4d", "#8b0000"], "diff": "Moderate"},
        "Reputation": {"color": "#C0C0C0", "bg_grad": ["#4a4a4a", "#000000"], "diff": "Hard"}
    }

    panic_lyrics = [
        "You’re on your own, kid. You always have been.",
        "Breathe in, breathe through, breathe deep, breathe out.",
        "Long story short, I survived.",
        "This is me trying.",
        "I’m doing good, I’m on some new shit."
    ]

    # ------------------ COMPONENTES UI ------------------

    # 1. Panic Button Logic
    def panic_action(e):
        lyric = random.choice(panic_lyrics)
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"🚨 {lyric}", weight="bold", color="white"),
            bgcolor="#8B0000",
            duration=4000
        )
        page.snack_bar.open = True
        page.update()

    panic_btn = ft.FloatingActionButton(
        icon=ft.icons.WARNING_AMBER_ROUNDED,
        bgcolor="#8B0000",
        on_click=panic_action,
        tooltip="Panic Button"
    )
    page.floating_action_button = panic_btn

    # 2. Video Celebration Dialog
    # Asegúrate de tener 'taylor_wink.mp4' dentro de una carpeta 'assets'
    video_dialog = ft.AlertDialog(
        content=ft.Container(
            content=ft.Video(
                media=ft.VideoMedia("taylor_wink.mp4"),
                autoplay=True,
                expand=True
            ),
            width=300,
            height=300,
            border_radius=10,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS
        ),
        title=ft.Text("Task Completed! ✨", text_align="center")
    )

    def mark_as_done(e):
        # Muestra el video de celebración
        page.dialog = video_dialog
        video_dialog.open = True
        # Borra la tarea de la lista visualmente (opcional)
        task_list.controls.remove(e.control.parent.parent.parent) 
        page.update()

    # 3. Función para determinar el "Lyrics Mood"
    def get_lyrics_mood(days_left):
        if days_left > 7:
            return "Life is a classroom... (Chill) 🌸"
        elif days_left > 3:
            return "It's nice to have a friend... (Focus) ☕"
        elif days_left > 0:
            return "I think I've seen this film before... (Warning) 🍂"
        else:
            return "BABY, LET THE GAMES BEGIN! (PANIC) 🐍"

    # 4. Gráfico de Carga de Trabajo (Workload Chart)
    # Una representación visual simple usando contenedores animados
    chart_row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, height=100, cross_alignment=ft.CrossAxisAlignment.END)
    
    def update_chart():
        chart_row.controls.clear()
        # Simulamos los días de la semana con barras de progreso vertical
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for day in days:
            # Altura aleatoria para simular carga de trabajo (en tu app final, esto dependerá de las tareas)
            load_height = random.randint(20, 100) 
            chart_row.controls.append(
                ft.Column([
                    ft.Container(
                        width=20, 
                        height=load_height, 
                        bgcolor="#C0C0C0", 
                        border_radius=5,
                        animate=ft.animation.Animation(500, "easeOut")
                    ),
                    ft.Text(day, size=10, color="grey")
                ], alignment=ft.MainAxisAlignment.END, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )

    # 5. Lista de Tareas
    task_list = ft.Column(spacing=15)

    def add_task(e):
        if not task_name.value or not date_picker.value:
            return

        selected_era = era_dropdown.value
        era_data = eras_config[selected_era]
        
        # Calcular tiempo restante (Countdown mock para el ejemplo)
        # Asumimos que la fecha del picker es el deadline
        deadline = datetime.datetime.strptime(str(date_picker.value).split(" ")[0], "%Y-%m-%d")
        now = datetime.datetime.now()
        delta = deadline - now
        days_left = delta.days

        lyrics_mood = get_lyrics_mood(days_left)

        # Crear la tarjeta de la tarea (Card)
        new_task = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Checkbox(on_change=mark_as_done, fill_color=era_data["color"]),
                    ft.Text(task_name.value, weight="bold", size=18, color="white"),
                ]),
                ft.Text(f"Deadline: {deadline.strftime('%b %d, %Y')} | {days_left} days left", size=12, color="white70"),
                ft.ProgressBar(value=max(0.1, 1 - (days_left/14)), color=era_data["color"], bgcolor="black26"),
                ft.Text(f"Mood: {lyrics_mood}", size=11, italic=True, color="white")
            ]),
            padding=15,
            border_radius=15,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=era_data["bg_grad"]
            ),
            animate=ft.animation.Animation(300, "easeIn")
        )

        task_list.controls.append(new_task)
        task_name.value = ""
        update_chart() # Actualiza el gráfico visualmente
        page.update()

    # ------------------ INTERFAZ DE ENTRADA ------------------
    
    header = ft.Text("My Academic Eras", size=32, weight="bold", italic=True, color="#C0C0C0")
    
    task_name = ft.TextField(label="Assignment Name", border_color="grey")
    
    era_dropdown = ft.Dropdown(
        label="Select Era (Difficulty)",
        options=[
            ft.dropdown.Option("Lover"),
            ft.dropdown.Option("Red"),
            ft.dropdown.Option("Reputation"),
        ],
        value="Lover",
        border_color="grey"
    )

    # Date Picker para el Deadline
    date_picker = ft.DatePicker(
        on_change=lambda e: date_btn.update()
    )
    page.overlay.append(date_picker)
    
    date_btn = ft.ElevatedButton(
        "Pick Deadline",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda e: date_picker.pick_date()
    )

    add_btn = ft.ElevatedButton("Add Assignment", bgcolor="#C0C0C0", color="black", on_click=add_task)

    # ------------------ RENDERIZAR TODO ------------------
    update_chart() # Inicializar gráfico

    page.add(
        header,
        ft.Divider(color="grey"),
        ft.Text("Weekly Workload", weight="bold", size=16),
        chart_row,
        ft.Divider(color="grey"),
        task_name,
        era_dropdown,
        ft.Row([date_btn, add_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(color="transparent", height=10),
        ft.Text("Upcoming Deadlines", weight="bold", size=20),
        task_list
    )

ft.app(target=main, assets_dir="assets")