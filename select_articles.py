import json

with open('/root/.hermes/_build/articles_data.json', 'r') as f:
    data = json.load(f)

articles = data['articles']
target_pmids = [
    "42595326", # Vascular: Recurrent nontraumatic acute subdural hematoma secondary to ruptured accessory meningeal artery aneurysm
    "42595109", # Neuro-oncology: TIMELESS promotes glioma stemness and malignancy through JAK-STAT3 pathway
    "42595494", # Functional: Subthalamic Nucleus Deep Brain Stimulation Enhanced Long-Latency Reflex II in Parkinson's Disease
    "42594313", # Spine: Influence of Preoperative Mental Health on Surgical and Clinical Outcomes in Degenerative Cervical Myelopathy
    "42592584", # Skull Base: Preliminary Clinical Experience With a Novel Foamy Collagen-Based Dural Substitute (Foamagen)
    "42594036", # Neurotrauma: Delayed External Brain Tamponade Following Repeat Craniectomy
    "42595102", # Peripheral/Cranial Nerve: A standardized, surgically relevant map for emergence of organ-specific branches from the human vagus nerve
    "42593631", # Pain: Sinomenine Liposomes Alleviate Neuropathic Pain in a Spared Nerve Injury Model by Regulating Astrocyte Reactivity
    "42595299", # Hydrocephalus/Ventricular: Electromagnetic navigation and ventricular catheter placement
    "42595329"  # Neurovascular/Stroke: Willisian collateral and carotid stenosis during large vessel occlusion stroke
]

selected = [a for a in articles if a['pmid'] in target_pmids]
print(f"Found {len(selected)} articles")
for s in selected:
    print(s['pmid'], s['title'])
