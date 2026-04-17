import flet as ft
import datetime
import random
import traceback
import sys

def main(page: ft.Page):
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
        "Reputation": {"color": "#C0C0C0", "bg_grad": ["#4a4a4a", "#000000"], "diff": "Hard"},
    }

    panic_lyrics = [
        "You're on your own, kid. You always have been.",
        "Breathe in, breathe through, breathe deep, breathe out.",
        "Long story short, I survived.",
        "This is me trying.",
        "I'm doing good, I'm on some new shit.",
    ]

    # Panic Button
    def panic_action(e):
        lyric = random.choice(panic_lyrics)
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"🚨 {lyric}", weight="bold", color="white"),
            bgcolor="#8B0000",
            duration=4000,
        )
        page.snack_bar.open = True
        page.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.WARNING_AMBER_ROUNDED,
        bgcolor="#8B0000",
        on_click=panic_action,
        tooltip="Panic Button",
    )

    # Lyrics Mood
    def get_lyrics_mood(days_left):
        if days_left > 7:
            return "Life is a classroom... (Chill) 🌸"
        elif days_left > 3:
            return "It's nice to have a friend... (Focus) ☕"
        elif days_left > 0:
            return "I think I've seen this film before... (Warning) 🍂"
        else:
            return "BABY, LET THE GAMES BEGIN! (PANIC) 🐍"

    # Chart
    chart_row = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        height=100,
        cross_alignment=ft.CrossAxisAlignment.END,
    )

    def update_chart():
        chart_row.controls.clear()
        days_label = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_counts = [0] * 7
        for task_data in tasks_data:
            weekday = task_data["deadline"].weekday()
            day_counts[weekday] += 1
        max_count = max(day_counts) if any(day_counts) else 1
        for i, day in enumerate(days_label):
            load_height = max(8, int((day_counts[i] / max_count) * 90))
            chart_row.controls.append(
                ft.Column(
                    [
                        ft.Container(
                            width=20,
                            height=load_height,
                            bgcolor="#C0C0C0",
                            border_radius=5,
                            animate=ft.animation.Animation(500, "easeOut"),
                        ),
                        ft.Text(day, size=10, color="grey"),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

    # Tasks
    task_list = ft.Column(spacing=15)
    tasks_data = []

    def add_task(e):
        if not task_name.value or not date_picker.value or not era_dropdown.value:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("⚠️ Please fill in all fields.", color="white"),
                bgcolor="#555555",
                duration=2500,
            )
            page.snack_bar.open = True
            page.update()
            return

        selected_era = era_dropdown.value
        era_data = eras_config[selected_era]
        deadline = datetime.datetime.strptime(str(date_picker.value).split(" ")[0], "%Y-%m-%d")
        now = datetime.datetime.now()
        days_left = (deadline - now).days
        lyrics_mood = get_lyrics_mood(days_left)
        progress_value = max(0.0, min(1.0, 1 - (days_left / 14)))

        new_task_ref = [None]

        def mark_as_done(e):
            # Solo quitamos la tarea (sin video)
            if new_task_ref[0] in task_list.controls:
                task_list.controls.remove(new_task_ref[0])

            tasks_data[:] = [t for t in tasks_data if t["deadline"] != deadline or t["name"] != task_name_val]
            update_chart()
            page.update()

        task_name_val = task_name.value
        new_task = ft.Container(
            content=ft.Column([
                ft.Row([ft.Checkbox(on_change=mark_as_done, fill_color=era_data["color"]),
                        ft.Text(task_name_val, weight="bold", size=18, color="white")]),
                ft.Text(f"Deadline: {deadline.strftime('%b %d, %Y')} | {days_left} days left",
                        size=12, color="white70"),
                ft.ProgressBar(value=progress_value, color=era_data["color"], bgcolor="black26"),
                ft.Text(f"Mood: {lyrics_mood}", size=11, italic=True, color="white"),
            ]),
            padding=15,
            border_radius=15,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=era_data["bg_grad"],
            ),
        )

        new_task_ref[0] = new_task
        task_list.controls.append(new_task)
        tasks_data.append({"name": task_name_val, "deadline": deadline})

        task_name.value = ""
        date_picker.value = None
        date_btn.text = "Pick Deadline"
        update_chart()
        page.update()

    # ------------------ INTERFAZ ------------------
    header = ft.Text("My Academic Eras", size=32, weight="bold", italic=True, color="#C0C0C0")

    task_name = ft.TextField(label="Assignment Name", border_color="grey")
    era_dropdown = ft.Dropdown(
        label="Select Era (Difficulty)",
        options=[
            ft.dropdown.Option("Lover"),
            ft.dropdown.Option("Red"),
            ft.dropdown.Option("Reputation")
        ],
        value="Lover",
        border_color="grey",
    )

    def on_date_change(e):
        if date_picker.value:
            date_btn.text = date_picker.value.strftime("%b %d, %Y")
            page.update()

    date_picker = ft.DatePicker(on_change=on_date_change)
    page.overlay.append(date_picker)

    date_btn = ft.ElevatedButton(
        "Pick Deadline", 
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda e: date_picker.pick_date()
    )

    add_btn = ft.ElevatedButton(
        "Add Assignment", 
        bgcolor="#C0C0C0", 
        color="black", 
        on_click=add_task
    )

    # Render
    update_chart()

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
        task_list,
    )


# ====================== ERROR HANDLER ======================
def global_error_handler(e):
    error_text = f"Error:\n{str(e)}\n\n{traceback.format_exc(limit=15)}"
    
    error_page = ft.Page()
    error_page.title = "Error"
    error_page.bgcolor = ft.Colors.RED_900
    error_page.vertical_alignment = ft.MainAxisAlignment.CENTER
    error_page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    error_page.padding = 30

    error_page.add(
        ft.Column([
            ft.Icon(ft.Icons.ERROR_OUTLINE_ROUNDED, color=ft.Colors.WHITE, size=90),
            ft.Text("¡La app falló al iniciar!", size=24, color=ft.Colors.WHITE, weight="bold"),
            ft.Container(
                content=ft.Text(error_text, color=ft.Colors.WHITE70, size=13),
                bgcolor=ft.Colors.BLACK26,
                padding=15,
                border_radius=10,
                width=380,
            ),
            ft.ElevatedButton("Cerrar", bgcolor=ft.Colors.WHITE, color=ft.Colors.RED_900,
                              on_click=lambda _: sys.exit(0))
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
    )
    
    ft.app(target=lambda p: error_page)

# ====================== INICIO ======================
if __name__ == "__main__":
    try:
        ft.app(target=main, assets_dir="assets")
    except Exception as ex:
        global_error_handler(ex)
