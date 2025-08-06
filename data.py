import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import datetime
import dateutil
from dateutil import parser

class Data:
    def __init__(self, path):
        self.path = path
        self.artists = []
        self.songs = []
        self.main_year = 0
        
        # Load and combine all JSON files
        files = glob.glob(os.path.join(path, "*.json"))
        df_list = [pd.read_json(f, encoding='utf-8') for f in files]
        self.data = pd.concat(df_list, ignore_index=False)
        
        # Calculate basic stats
        self.total_cols = self.data.shape[1]
        self.total_rows = self.data.shape[0]
        self.total_listened = self.data['ms_played'].sum()

    def getDataForYear(self, year):
        if year == 'All Time':
            return self.data
        else:
            year = int(year)
            return self.data[self.data['ts'].apply(lambda x: parser.parse(x).year) == year]

    def get_Years(self) -> list:
        years = self.data['ts'].apply(lambda x: parser.parse(x).year).unique().tolist()
        years.sort() 
        return years
    
    def getTotalListeningTime(self, df):
        return (df['ms_played'].sum())
    
    def getTotalTracks(self, df):
        return str(df.shape[0])
    
    def getUniqueArtists(self, df):
        return f"{len(df['master_metadata_album_artist_name'].unique()):,}"
    
    def getSkipRate(self, df):
     
        return f"{ df['skipped'].values.sum()/df.shape[0]*100:.0f}%" 
    
    def getTopSongs(self, df):
        top_songs = df.groupby(['master_metadata_track_name', 'master_metadata_album_artist_name'])['ms_played'].sum().reset_index().sort_values(by='ms_played', ascending=False).head(10)
        top_songs['minutes_played'] = top_songs['ms_played'] / 60000
        songs_data = []
        i=0
        for _, row in top_songs.iterrows():
            i+=1
            songs_data.append([
                i,
                row['master_metadata_track_name'],
                row['master_metadata_album_artist_name'],
                f"{row['minutes_played']:.1f}"
            ])
        print(songs_data)
        return songs_data
        
    def getTopArtists(self, df):
        top_artists = df.groupby('master_metadata_album_artist_name')['ms_played'].sum().reset_index().sort_values(by='ms_played', ascending=False).head(10)
        top_artists['minutes_played'] = top_artists['ms_played'] / 60000
        artists_data = []
        i=0
        for _, row in top_artists.iterrows():
            i+=1
            artists_data.append([
                i,
                row['master_metadata_album_artist_name'],
                f"{row['minutes_played']:.1f}"
            ])
        print(artists_data)
        return artists_data