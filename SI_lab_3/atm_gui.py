# atm_gui.py
# Interfaz gráfica para el Cajero ATM usando Tkinter
# Requiere: atm.py en el mismo directorio

import tkinter as tk
from tkinter import messagebox
from atm import Atm, SaldoInsuficienteError, MontoInvalidoError

# ─── Colores y fuentes ───────────────────────────────────────────────────────
BG_DARK    = "#1a1a2e"
BG_CARD    = "#16213e"
BG_PANEL   = "#0f3460"
ACCENT     = "#e94560"
TEXT_WHITE = "#eaeaea"
TEXT_GRAY  = "#a8a8b3"

BTN_GREEN  = "#00b894"
BTN_RED    = "#d63031"
BTN_BLUE   = "#0984e3"

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_SUB   = ("Segoe UI", 11)
FONT_MONO  = ("Consolas", 13)
FONT_BIG   = ("Segoe UI", 26, "bold")


class AtmApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Cajero Automático ATM")
        self.geometry("620x520")
        self.resizable(False, False)
        self.configure(bg=BG_DARK)

        self._cajero = Atm(
            titular="Cliente ATM",
            saldo_inicial=1000.0
        )

        self._build_ui()
        self._refresh_saldo()

    # ──────────────────────────────────────────────────────────────────────
    # Construcción de interfaz
    # ──────────────────────────────────────────────────────────────────────
    def _build_ui(self):

        # ── Encabezado ───────────────────────────────────────────────────
        header = tk.Frame(
            self,
            bg=BG_PANEL,
            padx=20,
            pady=14
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="🏧  CAJERO AUTOMÁTICO ATM",
            font=FONT_TITLE,
            bg=BG_PANEL,
            fg=TEXT_WHITE
        ).pack(side="left")

        # ── Tarjeta saldo ────────────────────────────────────────────────
        card = tk.Frame(
            self,
            bg=BG_CARD,
            padx=30,
            pady=20
        )
        card.pack(
            fill="x",
            padx=20,
            pady=(16, 8)
        )

        tk.Label(
            card,
            text="Saldo disponible",
            font=FONT_SUB,
            bg=BG_CARD,
            fg=TEXT_GRAY
        ).pack(anchor="w")

        self._lbl_saldo = tk.Label(
            card,
            text="S/ 0.00",
            font=FONT_BIG,
            bg=BG_CARD,
            fg=ACCENT
        )
        self._lbl_saldo.pack(anchor="w")

        tk.Label(
            card,
            text=f"Titular: {self._cajero.titular}",
            font=FONT_SUB,
            bg=BG_CARD,
            fg=TEXT_GRAY
        ).pack(
            anchor="w",
            pady=(6, 0)
        )

        # ── Entrada de monto ────────────────────────────────────────────
        input_frame = tk.Frame(
            self,
            bg=BG_DARK,
            padx=20,
            pady=4
        )
        input_frame.pack(fill="x")

        tk.Label(
            input_frame,
            text="Monto (S/):",
            font=FONT_SUB,
            bg=BG_DARK,
            fg=TEXT_WHITE
        ).pack(side="left")

        self._entry = tk.Entry(
            input_frame,
            font=FONT_MONO,
            width=12,
            bg=BG_CARD,
            fg=TEXT_WHITE,
            insertbackground=TEXT_WHITE,
            relief="flat",
            bd=6
        )

        self._entry.pack(
            side="left",
            padx=(8, 0)
        )

        self._entry.bind(
            "<Return>",
            lambda e: self._depositar()
        )

        # ── Botones ─────────────────────────────────────────────────────
        btn_frame = tk.Frame(
            self,
            bg=BG_DARK,
            padx=20,
            pady=10
        )
        btn_frame.pack(fill="x")

        btn_cfg = {
            "font": FONT_SUB,
            "relief": "flat",
            "cursor": "hand2",
            "padx": 18,
            "pady": 8,
            "bd": 0
        }

        tk.Button(
            btn_frame,
            text="💰 Depositar",
            bg=BTN_GREEN,
            fg="white",
            activebackground=BTN_GREEN,
            activeforeground="white",
            command=self._depositar,
            **btn_cfg
        ).pack(
            side="left",
            padx=(0, 8)
        )

        tk.Button(
            btn_frame,
            text="💸 Retirar",
            bg=BTN_RED,
            fg="white",
            activebackground=BTN_RED,
            activeforeground="white",
            command=self._retirar,
            **btn_cfg
        ).pack(
            side="left",
            padx=(0, 8)
        )

        tk.Button(
            btn_frame,
            text="🔍 Consultar",
            bg=BTN_BLUE,
            fg="white",
            activebackground=BTN_BLUE,
            activeforeground="white",
            command=self._consultar,
            **btn_cfg
        ).pack(side="left")

        # ── Historial ───────────────────────────────────────────────────
        hist_frame = tk.Frame(
            self,
            bg=BG_DARK,
            padx=20,
            pady=16
        )

        hist_frame.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            hist_frame,
            text="Historial de operaciones",
            font=FONT_SUB,
            bg=BG_DARK,
            fg=TEXT_GRAY
        ).pack(anchor="w")

        text_container = tk.Frame(
            hist_frame,
            bg=BG_DARK
        )

        text_container.pack(
            fill="both",
            expand=True,
            pady=(6, 0)
        )

        self._txt = tk.Text(
            text_container,
            height=9,
            font=("Consolas", 10),
            bg=BG_CARD,
            fg=TEXT_WHITE,
            relief="flat",
            state="disabled",
            bd=6,
            wrap="word"
        )

        self._txt.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll = tk.Scrollbar(
            text_container,
            command=self._txt.yview
        )

        scroll.pack(
            side="right",
            fill="y"
        )

        self._txt.configure(
            yscrollcommand=scroll.set
        )

    # ──────────────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────────────
    def _refresh_saldo(self):
        self._lbl_saldo.config(
            text=f"S/ {self._cajero.saldo:,.2f}"
        )

    def _log(self, msg: str):

        self._txt.config(state="normal")

        self._txt.insert(
            "end",
            msg + "\n"
        )

        self._txt.see("end")

        self._txt.config(state="disabled")

    def _get_monto(self):

        raw = self._entry.get().strip()

        if not raw:
            messagebox.showwarning(
                "Campo vacío",
                "Ingrese un monto."
            )
            return None

        try:
            val = float(raw)

        except ValueError:

            messagebox.showerror(
                "Error",
                "Ingrese un número válido."
            )

            return None

        self._entry.delete(0, "end")

        return val

    # ──────────────────────────────────────────────────────────────────────
    # Acciones
    # ──────────────────────────────────────────────────────────────────────
    def _depositar(self):

        monto = self._get_monto()

        if monto is None:
            return

        try:

            self._cajero.depositar(monto)

            self._refresh_saldo()

            self._log(
                f"[DEPÓSITO]  +S/{monto:.2f}  →  "
                f"Saldo: S/{self._cajero.saldo:,.2f}"
            )

        except MontoInvalidoError as e:

            messagebox.showerror(
                "Depósito rechazado",
                str(e)
            )

            self._log(
                f"[ERROR] Depósito S/{monto:.2f} rechazado: {e}"
            )

    def _retirar(self):

        monto = self._get_monto()

        if monto is None:
            return

        try:

            self._cajero.retirar(monto)

            self._refresh_saldo()

            self._log(
                f"[RETIRO]  -S/{monto:.2f}  →  "
                f"Saldo: S/{self._cajero.saldo:,.2f}"
            )

        except SaldoInsuficienteError as e:

            messagebox.showerror(
                "Saldo insuficiente",
                str(e)
            )

            self._log(
                f"[ERROR] Retiro S/{monto:.2f} rechazado: {e}"
            )

        except MontoInvalidoError as e:

            messagebox.showerror(
                "Retiro rechazado",
                str(e)
            )

            self._log(
                f"[ERROR] Retiro S/{monto:.2f} rechazado: {e}"
            )

    def _consultar(self):

        saldo = self._cajero.consultar_saldo()

        self._log(
            f"[CONSULTA] Saldo actual: S/{saldo:,.2f}"
        )

        messagebox.showinfo(
            "Saldo actual",
            f"Su saldo disponible es:\n\nS/ {saldo:,.2f}"
        )


# ──────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    app = AtmApp()
    app.mainloop()