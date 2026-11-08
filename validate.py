#!/usr/bin/env python3
"""Contrôles de cohérence des positions et liens sourcés du projet Fouju."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

actors=read("data/actors.json")
claims=read("data/claims.json")
relations=read("data/relations.json")
evidence=read("data/evidence.json")
sources=read("data/sources.json")
taxonomy=read("config/taxonomy.json")
synthesis=read("data/synthesis.json")
content=read("data/content.json")

def indexed(rows, kind):
    ids=[x["id"] for x in rows]
    assert len(ids)==len(set(ids)), f"Doublons d'ID : {kind}"
    return {x["id"]:x for x in rows}

A=indexed(actors,"acteurs")
C=indexed(claims,"positions")
R=indexed(relations,"relations")
E=indexed(evidence,"preuves")
S=indexed(sources,"sources")

def verified(ids, owner):
    assert ids, f"Aucune preuve : {owner}"
    for eid in ids:
        assert eid in E, f"Preuve introuvable {eid} : {owner}"
        sid=E[eid].get("source_id")
        assert sid in S, f"Source introuvable pour {eid} : {owner}"
        url=S[sid].get("url")
        assert isinstance(url,str) and url.startswith(("https://","http://")), f"URL absente : {owner}"

assert "project_fouju" in A
for actor in actors:
    if actor["id"] != "project_fouju":
        assert any(c["subject_id"]==actor["id"] for c in claims), f"Fiche sans documentation : {actor['id']}"
for x in claims:
    assert x["subject_id"] in A, x["id"]
    assert x["value"] in taxonomy["stances"] and x["value"]!="all", x["id"]
    verified(x.get("evidence_ids",[]),x["id"])
for x in relations:
    assert x["source_id"] in A and x["target_id"] in A, x["id"]
    verified(x.get("evidence_ids",[]),x["id"])
for field in ("griefs","vigilance"):
    for i,x in enumerate(synthesis[field]):
        verified(x.get("evidence_ids",[]),f"{field} {i}")
for field in ("milestones","fact_sheet"):
    for i,x in enumerate(content[field]):
        verified(x.get("evidence_ids",[]),f"{field} {i}")

print(f"OK — {len(A)} noeuds, {len(C)} fiches, {len(R)} relations, "
      f"{len(E)} preuves, {len(S)} sources et aucune reference non qualifiee")


# Contrôles de l'onglet Évolution des acteurs — 8 novembre 2026.
from datetime import date
import re
from urllib.parse import urlsplit

timeline=read("data/timeline.json")
T=indexed(timeline,"apparitions documentaires")
categories={item["id"] for item in taxonomy["timeline"]["categories"]}
assert taxonomy["timeline"]["event_type"]=="first_documented_appearance"
assert len(timeline)==len(A)-1,"La chronologie doit qualifier tous les acteurs hors projet central"
assert {item["actor_id"] for item in timeline}==set(A)-{"project_fouju"}
assert len({item["actor_id"] for item in timeline})==len(timeline),"Un même acteur apparaît plusieurs fois"

for event in timeline:
    assert event["actor_id"] in A and event["category"] in categories, event["id"]
    assert event["source_ids"],event["id"]
    verified(event["evidence_ids"],event["id"])
    for source_id in event["source_ids"]:
        assert source_id in S,event["id"]
        url=S[source_id].get("url") or ""
        parsed=urlsplit(url)
        assert parsed.scheme=="https" and parsed.netloc,event["id"]
    if event["status"]=="confirmed":
        moment=event["date"]
        precision=event["date_precision"]
        if precision=="day":
            assert re.fullmatch(r"\d{4}-\d{2}-\d{2}",moment),event["id"]
            assert date.fromisoformat(moment)<=date(2026,11,8),event["id"]
        elif precision=="month":
            assert re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])",moment),event["id"]
            assert date.fromisoformat(moment+"-01")<=date(2026,11,8),event["id"]
        else:
            raise AssertionError("Précision invalide "+event["id"])
    else:
        assert event["status"]=="undated" and event["date"] is None,event["id"]
        assert event["date_precision"]=="unknown",event["id"]

page=(ROOT/"apps/cards/index.html").read_text(encoding="utf-8")
tabs=("carto","griefs","watch","evolution","timeline")
for tab in tabs:
    assert f'data-tab="{tab}"' in page and f'id="tab-{tab}"' in page,tab
assert len(re.findall(r'data-tab="[^"]+"',page))==len(tabs)
for path in ("assets/js/evolution.js","assets/css/evolution.css"):
    assert (ROOT/path).is_file(),path
loader=(ROOT/"assets/js/data-loader.js").read_text(encoding="utf-8")
assert 'timeline:"data/timeline.json"' in loader
dated=sum(x["status"]=="confirmed" for x in timeline)
undated=len(timeline)-dated
print(f"ÉVOLUTION OK : {dated} acteurs datables, {undated} à qualifier, {len(tabs)} onglets ; preuves et URLs contrôlées.")
