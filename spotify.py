import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import DISABLED
from tkinter import font as tkfont
from data import Data
import pandas as pd

# For dark theme colors
BG_COLOR = '#181c23'
CARD_COLOR = '#232733'
TEXT_COLOR = '#b6fcd5'
LABEL_COLOR = '#b6fcd5'
BAR_COLOR = '#2ecc40'

class SpotifyStatsGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Spotify Listening Stats')
        self.configure(bg=BG_COLOR)
        self.geometry('800x900')
        self.resizable(False, False)
        self.custom_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        
        # Initialize data first
        self.data = Data("data_folder")
        self.years = self.data.get_Years()
        
        self._build_gui()

    def _build_card(self, parent, label, value, row, column):
        frame = tk.Frame(parent, bg=CARD_COLOR, bd=0, relief='flat')
        frame.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')
        label_widget = tk.Label(frame, text=label, bg=CARD_COLOR, fg=LABEL_COLOR, font=("Segoe UI", 12))
        label_widget.pack(anchor='w', padx=10, pady=(10,0))
        value_widget = tk.Entry(frame, font=self.custom_font, fg=TEXT_COLOR, bg=CARD_COLOR, bd=0, state=DISABLED, disabledforeground=TEXT_COLOR, disabledbackground=CARD_COLOR)
        value_widget.insert(0, value)
        value_widget.pack(anchor='w', padx=10, pady=(0,10))
        return value_widget

    def _format_listening_time(self, ms_played):
        hours = ms_played / (1000 * 60 * 60)
        if hours >= 1000:
            return f"{hours/1000:.1f}k hours"
        else:
            return f"{hours:.0f} hours"

    def _build_gui(self):
        total_listening_time = self._format_listening_time(self.data.total_listened)
        total_tracks = self.data.getTotalTracks(self.data.data)
        unique_artists = self.data.getUniqueArtists(self.data.data)
        top_songs = self.data.getTopSongs(self.data.data)
        top_artists = self.data.getTopArtists(self.data.data)
        skip_rate = self.data.getSkipRate(self.data.data)

        select_frame = tk.Frame(self, bg=BG_COLOR)
        select_frame.pack(fill='x', pady=(20, 0))
        tk.Label(select_frame, text='Show Data For:', bg=BG_COLOR, fg=LABEL_COLOR, font=("Segoe UI", 12)).pack(side='left', padx=(20, 5))
        self.period_var = StringVar(value='All Time')

        period_values = ['All Time'] + [str(year) for year in self.years]
        self.period_combo = ttk.Combobox(select_frame, textvariable=self.period_var, values=period_values, state='readonly', width=25)
        self.period_combo.pack(side='left')
        self.period_combo.bind('<<ComboboxSelected>>', self.on_cmb_select)

        # Top frame for stats
        stats_frame = tk.Frame(self, bg=BG_COLOR)
        stats_frame.pack(fill='x', pady=(20, 0))
        stats_frame.grid_columnconfigure((0,1), weight=1)
        stats_frame.grid_columnconfigure((2,3), weight=1)

        # cards
        self.total_listening_time_entry = self._build_card(stats_frame, 'Total Listening Time', total_listening_time, 0, 0)
        self.total_tracks_entry = self._build_card(stats_frame, 'Total Tracks Played', total_tracks, 0, 1)
        self.unique_artists_entry = self._build_card(stats_frame, 'Unique Artists', unique_artists, 0, 2)
        self.skip_rate_entry = self._build_card(stats_frame, 'Skip Rate', skip_rate, 0, 3)

        #  listboxes
        songs_listbox_frame = tk.Frame(self, bg=BG_COLOR)
        songs_listbox_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        tk.Label(songs_listbox_frame, text='Top Songs', bg=BG_COLOR, fg=LABEL_COLOR, font=("Segoe UI", 14, 'bold')).pack(pady=(0, 10))
        self.top_songs_listbox = tk.Listbox(songs_listbox_frame, bg=CARD_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 12), width=40)
        self.top_songs_listbox.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        for song in top_songs:
            self.top_songs_listbox.insert(tk.END, f"{song[0]}. {song[1]} - {song[2]} ({song[3]} minutes)")

        artists_listbox_frame = tk.Frame(self, bg=BG_COLOR)
        artists_listbox_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        tk.Label(artists_listbox_frame, text='Top Artists', bg=BG_COLOR, fg=LABEL_COLOR, font=("Segoe UI", 14, 'bold')).pack(pady=(0, 10))
        self.top_artists_listbox = tk.Listbox(artists_listbox_frame, bg=CARD_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 12), width=40)
        self.top_artists_listbox.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        for artist in top_artists:
            self.top_artists_listbox.insert(tk.END, f"{artist[0]}. {artist[1]} ({artist[2]} minutes)")

        # Listening Habits section
        artists_frame = tk.Frame(self, bg=BG_COLOR)
        artists_frame.pack(fill='x', pady=(30, 0))
        header = tk.Frame(artists_frame, bg=BG_COLOR)
        header.pack(fill='x')
        tk.Label(header, text='Listening Habits', bg=BG_COLOR, fg=LABEL_COLOR, font=("Segoe UI", 14, 'bold')).pack(side='left', padx=20)
        tk.Label(header, textvariable=self.period_var, bg=BG_COLOR, fg=LABEL_COLOR, font=("Segoe UI", 10)).pack(side='right', padx=20)

        # Placeholder for bar chart
        chart_frame = tk.Frame(artists_frame, bg=CARD_COLOR, height=300, width=700)
        chart_frame.pack(padx=20, pady=10, fill='x')
        chart_frame.pack_propagate(False)
        tk.Label(chart_frame, text='[Bar Chart Placeholder]', bg=CARD_COLOR, fg=BAR_COLOR, font=("Segoe UI", 16)).place(relx=0.5, rely=0.5, anchor='center')

    def on_cmb_select(self, event):
        selected_value = self.period_combo.get()
        df = self.data.getDataForYear(selected_value)
        
        # Update total listening time
        total_listening_time = self.data.getTotalListeningTime(df)
        formatted_time = self._format_listening_time(total_listening_time)
        self.total_listening_time_entry.config(state='normal')
        self.total_listening_time_entry.delete(0, 'end')
        self.total_listening_time_entry.insert(0, formatted_time)
        self.total_listening_time_entry.config(state='disabled')

        # Update totals
        total_tracks = self.data.getTotalTracks(df)
        self.total_tracks_entry.config(state='normal')
        self.total_tracks_entry.delete(0, 'end')
        self.total_tracks_entry.insert(0, total_tracks)
        self.total_tracks_entry.config(state='disabled')

        unique_artists = self.data.getUniqueArtists(df)

        self.unique_artists_entry.config(state='normal')
        self.unique_artists_entry.delete(0, 'end')
        self.unique_artists_entry.insert(0, unique_artists)
        self.unique_artists_entry.config(state='disabled')
        
        skip_rate = self.data.getSkipRate(df)

        self.skip_rate_entry.config(state='normal')
        self.skip_rate_entry.delete(0, 'end')
        self.skip_rate_entry.insert(0, skip_rate)
        self.skip_rate_entry.config(state='disabled')

        top_songs = self.data.getTopSongs(df)
        self.top_songs_listbox.delete(0, tk.END)
        for song in top_songs:
            self.top_songs_listbox.insert(tk.END, f"{song[0]}. {song[1]} - {song[2]} ({song[3]} minutes)")

        top_artists = self.data.getTopArtists(df)
        self.top_artists_listbox.delete(0, tk.END)
        for artist in top_artists:
            self.top_artists_listbox.insert(tk.END, f"{artist[0]}. {artist[1]} ({artist[2]} minutes)")

if __name__ == '__main__':
    app = SpotifyStatsGUI()
    app.mainloop()
