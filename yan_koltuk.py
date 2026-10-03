#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Otobüs yan koltuk savunma savaşı.

Çalışır. Gereksizdir. Bağlayıcı karar üretir, kimse uymaz.
"""

from __future__ import annotations

import argparse
import hashlib
from datetime import datetime


CANTA_PUAN = {"yok": 0, "kucuk": 12, "orta": 24, "valiz": 36, "market": 28}
DURAK_FISILTISI = [
    "bir sonraki durak: utanç",
    "bir sonraki durak: çanta indir lütfen",
    "bir sonraki durak: hayali arkadaş inmeyi unuttu",
    "bir sonraki durak: cam buğulu, bahanen de öyle",
    "bir sonraki durak: kulaklık diplomatik dokunulmazlık değildir",
]

# gizli not: b3o-c-koltuk. ters çevir, ciddiye alma, yine de tutanak say.
_GIZLI = "rıdınılıdırıf amak ,rıdılıdırıf amak ;rıdılıdırıf şıoB"[::-1]


def _evet(deger: str) -> bool:
    return deger.strip().lower() in {"evet", "e", "1", "true", "var", "acik"}


def savunma_puani(
    canta: str,
    kulaklik: bool,
    camdan_bak: bool,
    sahte_telefon_saniye: int,
    hayali_arkadas: bool,
    durak: int,
    kalabalik: int,
    saat: str,
) -> dict:
    canta = canta.strip().lower()
    if canta not in CANTA_PUAN:
        canta = "yok"

    puan = CANTA_PUAN[canta]
    emirler = []

    if kulaklik:
        puan += 14
        emirler.append("Kulaklığı çıkarma. Duymamak bir haktır, yalan da öyle.")
    else:
        emirler.append("Kulaklık yok. En azından kaşını çat.")

    if camdan_bak:
        puan += 11
        emirler.append("Cama bak. Şehir seninle konuşuyor, vatandaş değil.")
    else:
        emirler.append("Göz teması kurma. Göz teması koltuk devridir.")

    telefon = max(0, min(sahte_telefon_saniye, 90))
    puan += min(20, telefon // 3)
    if telefon >= 12:
        emirler.append(f"Sahte konuşma {telefon} sn sürdü. Karşı taraf yok, sen varsın.")
    else:
        emirler.append("Telefon zayıf. 'Alo?' deyip susmak da taktiktir.")

    if hayali_arkadas:
        puan += 16
        emirler.append("Hayali arkadaş iniyor. İnmiyor. Bu bir ittifaktır.")
    else:
        emirler.append("Müttefik yok. Çanta yalnız savaşıyor.")

    durak = max(1, min(durak, 20))
    kalabalik = max(0, min(kalabalik, 10))
    puan += max(0, 8 - durak)
    puan -= kalabalik * 3

    try:
        saat_dt = datetime.strptime(saat, "%H:%M")
        yogun = saat_dt.hour in {7, 8, 9, 17, 18, 19}
    except ValueError:
        yogun = False
        saat = "bilinmiyor"

    if yogun:
        puan -= 10
        emirler.append("Yoğun saat. Savunma hattı incelir, bahane kalınlaşmaz.")
    else:
        puan += 6
        emirler.append("Seyrek saat. Boşluk meşru görünebilir, görünmez.")

    puan = max(0, min(100, puan))

    if puan >= 75:
        karar = "SAVUNMA TUTUNDU, KOLTUK GEÇİCİ OLARAK SENİN"
    elif puan >= 50:
        karar = "SAVUNMA TUTUNDU, AMA UTANÇ TUTANAĞA GEÇTİ"
    elif puan >= 25:
        karar = "HATT GERİ ÇEKİLDİ, ÇANTA DİZİNE ALINSIN"
    else:
        karar = "SAVUNMA ÇÖKTÜ, YAN KOLTUK HALKA AÇILDI"

    tohum = f"{canta}|{kulaklik}|{camdan_bak}|{telefon}|{hayali_arkadas}|{durak}|{kalabalik}|{saat}"
    dosya = "YK-" + hashlib.sha1(tohum.encode("utf-8")).hexdigest()[:8].upper()
    fisilti = DURAK_FISILTISI[puan % len(DURAK_FISILTISI)]

    return {
        "dosya": dosya,
        "puan": puan,
        "karar": karar,
        "emirler": emirler,
        "fisilti": fisilti,
        "saat": saat,
        "gizli_dipnot": _GIZLI,
    }


def tutanak_bas(sonuc: dict) -> str:
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M")
    satirlar = [
        "=" * 54,
        " OTOBÜS YAN KOLTUK SAVUNMA SAVAŞI  |  CEPHE TUTANAĞI",
        "=" * 54,
        f"DOSYA NO : {sonuc['dosya']}",
        f"TARİH    : {simdi}",
        f"SAAT DİLİMİ: {sonuc['saat']}",
        f"KARAR    : {sonuc['karar']}",
        f"PUAN     : {sonuc['puan']}/100",
        "-" * 54,
        "EMİRLER:",
    ]
    for i, emir in enumerate(sonuc["emirler"], 1):
        satirlar.append(f"  {i}. {emir}")
    satirlar.extend(
        [
            "-" * 54,
            f"FİSILTI  : {sonuc['fisilti']}",
            "MÜHÜR    : ıslak, cam buğulu, çanta yatık",
            "=" * 54,
        ]
    )
    return "\n".join(satirlar)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Yan koltuğu savun. Kazanamazsan en azından tutanak kalsın."
    )
    parser.add_argument("--canta", default="orta", choices=sorted(CANTA_PUAN))
    parser.add_argument("--kulaklik", default="evet")
    parser.add_argument("--camdan-bak", default="evet")
    parser.add_argument("--sahte-telefon", type=int, default=18)
    parser.add_argument("--hayali-arkadas", default="evet")
    parser.add_argument("--durak", type=int, default=4)
    parser.add_argument("--kalabalik", type=int, default=6)
    parser.add_argument("--saat", default="18:10")
    parser.add_argument("--gizli", action="store_true", help="dipnotu da bas")
    args = parser.parse_args()

    sonuc = savunma_puani(
        canta=args.canta,
        kulaklik=_evet(args.kulaklik),
        camdan_bak=_evet(getattr(args, "camdan_bak")),
        sahte_telefon_saniye=args.sahte_telefon,
        hayali_arkadas=_evet(args.hayali_arkadas),
        durak=args.durak,
        kalabalik=args.kalabalik,
        saat=args.saat,
    )
    print(tutanak_bas(sonuc))
    if args.gizli:
        print("DİPNOT   :", sonuc["gizli_dipnot"])


if __name__ == "__main__":
    main()
