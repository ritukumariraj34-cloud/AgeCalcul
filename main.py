import flet as ft
from datetime import date, datetime

def main(page: ft.Page):
    page.title = "Age Calculator"
    # Changed from 'center' to 'start' to align everything at the top
    page.vertical_alignment = ft.MainAxisAlignment.START 
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = "dark"
    page.padding = 20

    # --- TOP APP BAR ---
    page.appbar = ft.AppBar(
        title=ft.Text("Age Calculator", weight="bold", color="white"),
        center_title=True,
        bgcolor="blue",
    )

    # UI Elements
    result_age = ft.Text(size=26, weight="bold", color="#42A5F5") 
    next_bday_text = ft.Text(size=18, color="white", weight="w500") 
    dob_text = ft.Text("No date selected", size=16, color="white70")

    def calculate_age(birth):
        if hasattr(birth, "date"):
            birth = birth.date()
            
        today = date.today()

        # 1. ACCURATE AGE CALCULATION (Exact Calendar Match)
        # Using the same logic as Period.between in your Kotlin app
        years = today.year - birth.year
        months = today.month - birth.month
        days = today.day - birth.day

        if days < 0:
            months -= 1
            # Accurate day borrowing based on the specific month length
            if today.month == 1:
                prev_month_days = 31 
            else:
                last_day_prev = date(today.year, today.month, 1).toordinal() - 1
                prev_month_days = date.fromordinal(last_day_prev).day
            days += prev_month_days

        if months < 0:
            years -= 1
            months += 12

        # 2. NEXT BIRTHDAY CALCULATION
        # Matches ChronoUnit logic from your app
        next_bday_date = date(today.year, birth.month, birth.day)
        
        if next_bday_date <= today:
            next_bday_date = date(today.year + 1, birth.month, birth.day)
        
        days_remaining = (next_bday_date - today).days

        # Update labels
        result_age.value = f"{years}y {months}m {days}d"
        next_bday_text.value = f"Next Birthday: {days_remaining} Days"
        dob_text.value = f"Born: {birth.strftime('%d %b %Y')}"
        page.update()

    def on_date_change(e):
        if e.control.value:
            try:
                val = e.control.value
                if isinstance(val, str):
                    birth = datetime.fromisoformat(val.split('T')[0]).date()
                else:
                    birth = val
                calculate_age(birth)
            except Exception:
                pass

    date_picker = ft.DatePicker(
        first_date=date(1900,1,1),
        last_date=date.today(),
        on_change=on_date_change
    )
    page.overlay.append(date_picker)

    def open_picker(e):
        date_picker.open = True
        page.update()

    # The Info Card for Results
    info_card = ft.Container(
        content=ft.Column([
            ft.Text("CALCULATED AGE", size=12, color="white54", weight="bold"),
            result_age,
            ft.Divider(height=20, color="white10"),
            next_bday_text,
        ], horizontal_alignment="center"),
        bgcolor="#1A1C1E", 
        padding=30,
        border_radius=20,
        border=ft.border.all(1, "white10"),
    )

    # Adding elements - they will now start from the top
    page.add(
        ft.Column([
            dob_text,
            ft.Button(
                "CHOOSE BIRTH DATE", 
                icon="calendar_month", 
                on_click=open_picker,
                color="blue",
            ),
            ft.Container(height=10), # Small gap
            info_card,
        ], 
        horizontal_alignment="center",
        spacing=15)
    )

if __name__ == "__main__":
    ft.run(main)
