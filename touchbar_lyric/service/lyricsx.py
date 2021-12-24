#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-16 09:10:24
# @Author  : Chenghao Mou (mouchenghao@gmail.com)


import os
from pathlib import Path
from thefuzz import process
from typing import List

from touchbar_lyric import Song
from loguru import logger

def lyricsx_music_search(title: str, artists: str) -> List[Song]:
    """
    Search from LyricsX with artists and title.
    Parameters
    ----------
    title : str
        Name of the song
    artists : str
        Names of the artists
    Returns
    -------
    List[Song]
        List of songs
    Examples
    --------
    >>> songs = lyricsx_music_search("海阔天空", "Beyond")
    >>> len(songs) > 0
    True
    >>> any(s.anchor(10) is not None for s in songs)
    True
    """
    score_cutoff: int = 90
    lyricsx_dir: str = os.getenv('LYRICSX_DIR')
    dir = Path(lyricsx_dir)
    assert dir.is_dir(), "Incorrect Lyricx directory: {}".format(lyricsx_dir)
    lrcx_files = dir.glob("*.lrcx")
    match_lrcx = process.extractOne("{} - {}".format(title, artists), [lr.name for lr in lrcx_files], score_cutoff=score_cutoff)

    songs = []
    if not match_lrcx:
        return songs

    lrcx, ratio = match_lrcx
    logger.debug("matched file {} with ratio {}".format(lrcx, ratio))

    lrp = dir / lrcx
    with open(lrp, 'r') as fr:
        content = fr.read()

    ltitle, lartists = lrp.stem.split(' - ')

    songs.append(
        Song(
            title=ltitle,
            artists=lartists,
            target_title=title,
            target_artists=artists,
            lyric=content,
        )
    )

    return songs
