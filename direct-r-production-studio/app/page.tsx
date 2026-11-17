'use client'

import { useEffect, useMemo, useState } from 'react'
import { Activity, ArrowRight, AudioLines, Bell, Check, ChevronDown, ChevronLeft, ChevronRight, CircleHelp, Clapperboard, Clock3, Database, Download, Eye, EyeOff, Film, FolderOpen, Gauge, Headphones, House, Layers3, MessageCircle, Mic2, MoreHorizontal, Music2, Play, Plus, Radio, RefreshCw, Search, Send, SlidersHorizontal, Sparkles, Volume2, WandSparkles, Zap } from 'lucide-react'

type Tab = 'Full Studio View' | '1. Screenplay & Lore' | '2. Visual & 3D Art' | '3. Audio & Soundscapes' | '4. Distribution Hub'
const tabs: Tab[] = ['Full Studio View', '1. Screenplay & Lore', '2. Visual & 3D Art', '3. Audio & Soundscapes', '4. Distribution Hub']
const defaultScenes = ['The Inciting Encounter', 'The Revelation & Confrontation', 'The Aftermath & Next Frontier']
const defaultStems = ['Ambient Sub-Drone', 'Atmospheric Pad', 'Rhythm Percussion', 'Distorted 808 Bass', 'Screaming Lead Synth']

function Panel({ title, eyebrow, icon: Icon, children, className = '' }: { title: string; eyebrow: string; icon: typeof Activity; children: React.ReactNode; className?: string }) {
  return (
    <section className={`panel ${className}`}>
      <div className="panel-head">
        <div className="panel-title-icon">
          <span className="panel-icon"><Icon size={15} /></span>
          <div>
            <div className="eyebrow">{eyebrow}</div>
            <h2>{title}</h2>
          </div>
        </div>
        <button className="icon-button" aria-label={`More ${title} options`} title="Panel options"><MoreHorizontal size={17} /></button>
      </div>
      {children}
    </section>
  )
}

function Header({ tension, setTension, onRun, onExport, backendConnected, projectTitle, projectGenre }: { tension: number; setTension: (v: number) => void; onRun: () => void; onExport: () => void; backendConnected: boolean; projectTitle: string; projectGenre: string }) {
  const mood = tension > .78 ? 'Climactic Crisis' : tension > .5 ? 'Rising Dread' : tension > .28 ? 'Unsettled' : 'Quiet Tension'
  return (
    <header className="topbar">
      <div className="brand-area">
        <div className="brand-mark"><Clapperboard size={17} strokeWidth={2.2} /></div>
        <div className="brand-name">Direct<span>R</span></div>
        <div className="active-pill" style={{ color: backendConnected ? '#10b981' : '#f59e0b' }}>
          <i style={{ background: backendConnected ? '#10b981' : '#f59e0b' }} /> {backendConnected ? 'BACKEND LIVE' : 'DEMO MODE'}
        </div>
      </div>
      <button className="project-select">
        <span className="project-kicker">CURRENT PRODUCTION</span>
        <strong>{projectTitle} <ChevronDown size={13} /></strong>
        <small>{projectGenre} <b>·</b> 5 min <b>·</b> 3 scenes <b>·</b> 2 characters</small>
      </button>
      <div className="pipeline">
        <div className="pipeline-label"><Activity size={12} /> AGENT PIPELINE</div>
        <div className="pipeline-nodes">
          <span><i className="dot cyan" />Narrative <small>{backendConnected ? 'Ready' : 'Mock'}</small></span>
          <b>›</b>
          <span><i className="dot pink" />Visual <small>{backendConnected ? 'Live' : 'Mock'}</small></span>
          <b>›</b>
          <span><i className="dot amber" />Audio <small>{backendConnected ? 'Live' : 'Mock'}</small></span>
          <b>›</b>
          <span><i className="dot green" />Creator <small>Online</small></span>
        </div>
      </div>
      <div className="header-actions">
        <div className="tension-control">
          <div className="tension-label">
            <span>MASTER TENSION</span>
            <strong>{tension.toFixed(2)} <em>— {mood}</em></strong>
          </div>
          <input aria-label="Global dramatic tension" type="range" min="0" max="1" step="0.01" value={tension} onChange={e => setTension(Number(e.target.value))} style={{'--range-fill': `${tension * 100}%`} as React.CSSProperties} />
        </div>
        <button className="export-button" onClick={onExport} title="Download production package"><Download size={14} /> Export</button>
        <button className="run-button" onClick={onRun}><Play size={13} fill="currentColor" /> Run Swarm</button>
      </div>
    </header>
  )
}

function NarrativePanel({ scene, setScene, onNpc, backendScenes, loading }: { scene: number; setScene: (v: number) => void; onNpc: () => void; backendScenes: any[]; loading?: boolean }) {
  const currentScene = backendScenes[scene] || null
  const sceneTitle = currentScene ? currentScene.title : defaultScenes[scene] || `Scene 0${scene + 1}`
  const location = currentScene ? currentScene.location : (scene === 1 ? 'Underground Cipher Vault' : scene === 2 ? 'Overlook Tower' : 'District 9 Lower Alleyway')
  const action = currentScene ? currentScene.action_description : (scene === 0 ? 'Rain needles the neon haze. LYRA VANCE stops beneath a flickering transit sign. Across the platform, a figure steps out of the static.' : scene === 1 ? 'Sparks fly from severed cables as security alarms blare in sync with the strobe lights.' : 'The storm has passed. Lyra watches dawn fracture across the skyline, carrying the weight of what they uncovered.')
  const dialogues = currentScene?.dialogue || []

  return (
    <Panel title="Story & Screenplay (Module 1)" eyebrow="01 / NARRATIVE AGENT (NVIDIA NEMOTRON)" icon={Clapperboard} className="narrative-panel">
      <div className="scene-tabs">
        {(backendScenes.length > 0 ? backendScenes : defaultScenes).map((item, i) => {
          const title = typeof item === 'string' ? item : item.title
          return (
            <button key={i} onClick={() => setScene(i)} className={scene === i ? 'scene-tab selected' : 'scene-tab'}>
              <span>0{i + 1}</span>{title}
            </button>
          )
        })}
      </div>
      <div className="script-sheet">
        <div className="script-meta">
          <span>INT. {location.toUpperCase()}</span>
          <span>{currentScene?.setting_time || 'NIGHT'} · CONTINUOUS</span>
        </div>
        <p className="action-copy">{action}</p>

        {dialogues.length > 0 ? (
          dialogues.map((dl: any, idx: number) => (
            <div key={idx} style={{ marginBottom: '12px' }}>
              <div className={`character-cue ${idx > 0 ? 'second' : ''}`}>
                {dl.speaker.toUpperCase()} <span>({dl.emotion} {dl.delivery_note ? `· ${dl.delivery_note}` : ''})</span>
              </div>
              <p className={`dialogue ${idx > 0 ? 'second-line' : ''}`}>
                “{dl.line}”
              </p>
            </div>
          ))
        ) : (
          <>
            <div className="character-cue">LYRA VANCE <span>(whispered · dialect adapted)</span></div>
            <p className="dialogue">
              “{scene === 0 ? "We can't stay here much longer. The perimeter is breached." : scene === 1 ? "Look closely at the cipher data. It doesn't lie!" : "We made it. I can't believe we are still standing."}”
            </p>
          </>
        )}

        <div className="script-footer">
          <span className="tag cyan-tag">● TENSION: {(currentScene?.tension_score ?? (scene === 1 ? 0.85 : scene === 2 ? 0.55 : 0.3)).toFixed(2)}</span>
          <span className="tag">DIALECT ENGINE: REALTIME</span>
          {currentScene?.foley_cues && currentScene.foley_cues.length > 0 && (
            <span className="tag amber-tag">FOLEY: {currentScene.foley_cues.length} CUES</span>
          )}
        </div>
      </div>
      <div className="narrative-bottom">
        <div className="integrity">
          <div className="avatar lyra">L</div>
          <div><strong>Lyra Vance</strong><small><Check size={10} /> Psychology: Historical records preserved</small></div>
          <div className="avatar kaelen">K</div>
          <div><strong>Kaelen Cross</strong><small><Check size={10} /> Psychology: Crew protection active</small></div>
        </div>
        <button className="npc-button" onClick={onNpc} disabled={loading}>
          <Sparkles size={13} /> {loading ? 'Synthesizing...' : 'Generate Reactive NPC'}
        </button>
      </div>
    </Panel>
  )
}

function VisualPanel({ tension, svgMarkup, anchorCount, turnaroundPrompt }: { tension: number; svgMarkup?: string; anchorCount?: number; turnaroundPrompt?: string }) {
  const [view, setView] = useState('Front')
  const [wire, setWire] = useState(true)
  const [showSvg, setShowSvg] = useState(false)
  const [layers, setLayers] = useState([true, true, true, true])
  const views = ['Front', '3/4 Perspective', 'Profile Side', 'Back View']
  const names = ['Background plate', 'Midground structures', 'Character layers', 'Neon lighting overlay']

  return (
    <Panel title="Visual Development (Module 2)" eyebrow="02 / VISUAL AGENT (LAYERED SVG & 3D TURNAROUNDS)" icon={Layers3} className="visual-panel">
      <div className="art-tabs">
        {views.map(v => (
          <button key={v} onClick={() => setView(v)} className={view === v ? 'art-tab active' : 'art-tab'}>{v}</button>
        ))}
        <button className={wire ? 'wire-button on' : 'wire-button'} onClick={() => setWire(!wire)}>
          <Activity size={12} /> Wireframe
        </button>
        <button className={showSvg ? 'wire-button on' : 'wire-button'} onClick={() => setShowSvg(!showSvg)}>
          <Layers3 size={12} /> {showSvg ? 'Concept Art' : 'Live Vector SVG'}
        </button>
      </div>
      <div className="artwork">
        {showSvg && svgMarkup ? (
          <div
            style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '16px' }}
            dangerouslySetInnerHTML={{ __html: svgMarkup }}
          />
        ) : (
          <img
            src="/lyra-neon.png"
            alt="Concept art of Lyra Vance in the rain-lit streets of Neo-Aethel"
            style={{ filter: `saturate(${.82 + tension * .5}) hue-rotate(${tension * -12}deg)` }}
          />
        )}
        {wire && !showSvg && (
          <div className="wire-overlay" aria-label="Rig-ready topology overlay">
            <span>RIG-READY TOPOLOGY · {view.toUpperCase()}</span>
            <i /><i /><i /><i /><i /><i /><i /><i /><i /><i /><i /><i />
          </div>
        )}
        <div className="art-view-label">TURNAROUND / {view.toUpperCase()}</div>
        <div className="art-count">{anchorCount || 16} <small>ANCHOR NODES</small></div>
      </div>
      {turnaroundPrompt && (
        <div style={{ padding: '8px 12px', background: 'rgba(255,255,255,0.02)', borderTop: '1px solid rgba(255,255,255,0.05)', fontSize: '11px', color: '#94a3b8' }}>
          <strong style={{ color: '#ec4899' }}>RIG TOPOLOGY:</strong> 4-angle orthogonal view · Clean edge loops · Neutral T-pose
        </div>
      )}
      <div className="layers-row">
        <strong>SVG VECTOR LAYERS</strong>
        <span>ANCHOR CONTROLLED</span>
      </div>
      <div className="layer-list">
        {names.map((name, i) => (
          <div key={name} className="layer-item">
            <button onClick={() => setLayers(layers.map((v, n) => n === i ? !v : v))} aria-label={`${layers[i] ? 'Hide' : 'Show'} ${name}`}>
              {layers[i] ? <Eye size={13} /> : <EyeOff size={13} />}
            </button>
            <span className="layer-handle">⠿</span>
            {name}
            <i className={`layer-color lc-${i}`} />
          </div>
        ))}
      </div>
      <div className="story-strip">
        <div className="strip-heading">STORYBOARD <span>03 FRAMES</span></div>
        <div className="story-frames">
          {defaultScenes.map((s, i) => (
            <button className="story-frame" key={s}>
              <img src="/lyra-neon.png" alt="" style={{objectPosition: `${30 + i * 30}% center`, filter: `hue-rotate(${i * 12}deg)`}} />
              <span>0{i + 1}</span>
              <small>{s}</small>
            </button>
          ))}
        </div>
      </div>
    </Panel>
  )
}

function AudioPanel({ tension, activeStems, liveBpm, foleyList }: { tension: number; activeStems: string[]; liveBpm?: number; foleyList?: any[] }) {
  const [levels, setLevels] = useState([70, 58, 42, 63, 36])
  const [preset, setPreset] = useState('Uncanny Neutral 3rd')
  const [playing, setPlaying] = useState('')
  const bpm = liveBpm || Math.round(65 + tension * 85)
  const stemsToShow = activeStems && activeStems.length > 0 ? activeStems : defaultStems
  const foley = foleyList && foleyList.length > 0 ? foleyList.map((f: any) => f.cue_name || f.cue) : ['SparksSizzle', 'RainOnRoof', 'VaultHum', 'SirenWail', 'HeartbeatPulse']

  return (
    <Panel title="Music & Sound Design (Module 3)" eyebrow="03 / AUDIO STUDIO (STEMS & FOLEY)" icon={AudioLines} className="audio-panel">
      <div className="audio-topline">
        <div><span className="eyebrow">SESSION TEMPO</span><strong className="bpm">{bpm}<small> BPM</small></strong></div>
        <div className="audio-live"><i /> ADAPTIVE TENSION MIX</div>
        <div className="sidechain"><span className="led" /> DIALOGUE DUCKING <b>−12 dB</b></div>
      </div>
      <div className="mixer">
        {stemsToShow.map((name, i) => (
          <div className="channel" key={name}>
            <div className="vu">
              <i style={{height: `${18 + ((i * 13 + bpm) % 63)}%`}} />
              <i style={{height: `${28 + ((i * 19 + bpm) % 58)}%`}} />
              <i style={{height: `${14 + ((i * 11 + bpm) % 66)}%`}} />
            </div>
            <div className="fader-wrap">
              <input type="range" min="0" max="100" value={levels[i % levels.length] + (i > 1 ? tension * 12 : 0)} aria-label={`${name} volume`} onChange={e => setLevels(levels.map((v, n) => n === (i % levels.length) ? Number(e.target.value) : v))} style={{'--range-fill': `${levels[i % levels.length]}%`} as React.CSSProperties} />
              <div className="fader-track" />
            </div>
            <span className="channel-name">{name.replace(/_/g, ' ')}</span>
            <span className="channel-db">{((levels[i % levels.length] || 50) / 10 - 10).toFixed(1)} dB</span>
          </div>
        ))}
      </div>
      <div className="audio-divider" />
      <div className="foley-section">
        <div className="foley-title"><span>ZERO-SHOT SYNTHESIZED FOLEY</span><small>CLICK TO AUDITION</small></div>
        <div className="foley-buttons">
          {foley.map((sound: string, i: number) => (
            <button key={sound} onClick={() => { setPlaying(sound); window.setTimeout(() => setPlaying(''), 1100) }} className={playing === sound ? 'foley-button playing' : 'foley-button'} title={`Preview ${sound}`}>
              <span>{['ϟ', '〰', '⌁', '⌘', '◉'][i % 5]}</span>{sound}
            </button>
          ))}
        </div>
      </div>
      <div className="harmony">
        <div className="foley-title"><span>24-EDO HARMONIC TUNING</span><small>MICROTONAL SCALES</small></div>
        <div className="harmony-options">
          {['Uncanny Neutral 3rd', 'Dystopian Paranoia', 'Cyber Mysticism', 'Crisis Cluster'].map((label, i) => (
            <button key={label} onClick={() => setPreset(label)} className={preset === label ? 'harmony-chip chosen' : 'harmony-chip'}>
              {label}<small>{['350¢ · 261.63 Hz', '150¢ · 233.08 Hz', '470¢ · 277.18 Hz', '100¢ · 220.00 Hz'][i]}</small>
            </button>
          ))}
        </div>
      </div>
    </Panel>
  )
}

function CreatorPanel() {
  const [posted, setPosted] = useState(false)
  const [variant, setVariant] = useState(0)
  const titles = ['THE TRUTH ABOUT NEO-AETHEL', 'DON’T WATCH THIS ALONE…', 'THEY TRIED TO HIDE THIS']
  return (
    <Panel title="Creator & distribution" eyebrow="04 / CREATOR AGENT" icon={Radio} className="creator-panel">
      <div className="creator-grid">
        <div className="reel-area">
          <div className="subsection-title">VERTICAL REEL <span>9:16 PREVIEW</span></div>
          <div className="phone">
            <img src="/lyra-neon.png" alt="Vertical reel preview featuring Lyra in Neo-Aethel" />
            <div className="phone-shade" />
            <div className="reel-top"><span>DIRECTR ORIGINAL</span><MoreHorizontal size={15} /></div>
            <div className="viral-hook">THE MOMENT<br />EVERYTHING<br /><b>CHANGED</b></div>
            <div className="reel-subtitle">“It was never a weapon.”</div>
            <div className="reel-bottom"><span><AudioLines size={14} /> ORIGINAL AUDIO</span><span>00:14 <i /> 00:32</span></div>
          </div>
          <div className="peak-badge"><Zap size={12} /> TENSION PEAK <strong>00:14s</strong><span>0.{Math.round(78 + variant * 4)}</span></div>
        </div>
        <div className="thumb-area">
          <div className="subsection-title">THUMBNAIL LAB <span>A/B/C TEST</span></div>
          <div className="thumb-list">
            {titles.map((title, i) => (
              <button key={title} onClick={() => setVariant(i)} className={variant === i ? 'thumb-card selected' : 'thumb-card'}>
                <div className="thumb-img">
                  <img src="/lyra-neon.png" alt="" style={{filter: `hue-rotate(${i * 22}deg)`}} />
                  {i === 0 && <div className="heatmap" />}
                </div>
                <div className="thumb-details">
                  <strong>{title}</strong>
                  <span><b>{['92.5', '87.2', '78.0'][i]}</b> / 100 <small>CTR {['14.8', '11.4', '9.6'][i]}%</small></span>
                </div>
                <em>VARIANT {String.fromCharCode(65 + i)}</em>
              </button>
            ))}
          </div>
        </div>
      </div>
      <div className="inbox">
        <div className="inbox-head"><div className="subsection-title">COMMUNITY INBOX <span>LIVE</span></div><span className="inbox-count">2 NEW</span></div>
        <div className="comment">
          <div className="comment-avatar">YT</div>
          <div className="comment-body">
            <div><strong>@neonpilgrim</strong><span className="sentiment">POSITIVE</span></div>
            <p>the score in that vault scene is unreal. need the full soundtrack.</p>
            <div className="ai-reply"><Sparkles size={11} /><span>That sound is the city remembering. Full score soon.</span>{posted && <b>POSTED</b>}</div>
          </div>
        </div>
        <div className="comment">
          <div className="comment-avatar tt">TT</div>
          <div className="comment-body">
            <div><strong>@aethel.afterdark</strong><span className="sentiment neutral">CURIOUS</span></div>
            <p>wait—who was the voice in the transmission?</p>
            <div className="ai-reply"><Sparkles size={11} /><span>Some secrets are better heard twice.</span></div>
          </div>
        </div>
        <button className="post-reply" onClick={() => setPosted(!posted)}><Send size={12} /> {posted ? 'Reply posted' : 'Post AI reply'} <span>2 queued</span></button>
      </div>
    </Panel>
  )
}

function RunModal({ step, onClose }: { step: number; onClose: () => void }) {
  const log = [
    'Narrative Agent (Module 1) — Dialogue & psychology constraints validated',
    'Visual Agent (Module 2) — 3 scene boards, turnarounds & vector paths generated',
    'Audio Studio (Module 3) — Tension stems & zero-shot foley synchronized',
    'Creator Agent (Module 4) — Vertical reels & A/B heatmap package assembled'
  ]
  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <section className="run-modal" role="dialog" aria-modal="true" aria-labelledby="run-title" onClick={e => e.stopPropagation()}>
        <div className="modal-top">
          <div className="modal-icon"><WandSparkles size={17} /></div>
          <button className="icon-button" onClick={onClose} aria-label="Close pipeline status">×</button>
        </div>
        <div className="eyebrow">AUTONOMOUS PRODUCTION</div>
        <h2 id="run-title">Swarm pipeline</h2>
        <p className="modal-copy">Creative agents are synthesizing your story, visual vectors, and soundscape.</p>
        <div className="progress-track"><i style={{width: `${step * 25}%`}} /></div>
        <div className="step-count">STEP {Math.min(step, 4)} OF 4 <span>{step >= 4 ? 'COMPLETE' : 'PROCESSING'}</span></div>
        <div className="execution-log">
          {log.map((item, i) => (
            <div key={item} className={i < step ? 'log-line completed' : 'log-line'}>
              <span>{i < step ? <Check size={12} /> : <i />}</span>{item}
              {i === step - 1 && step < 4 && <small>DONE</small>}
            </div>
          ))}
        </div>
        <button className="modal-done" onClick={onClose}>{step >= 4 ? 'Return to studio' : 'Run in background'} <ChevronRight size={14} /></button>
      </section>
    </div>
  )
}

function LandingPage({ onEnter }: { onEnter: (destination?: Tab) => void }) {
  const bars = [35, 24, 50, 72, 88, 42, 66, 48]
  const agents: { name: string; detail: string; color: string; icon: typeof Activity; tab: Tab }[] = [
    { name: 'Narrative Agent', detail: 'character constraints & dialect rules (Module 1)', color: 'cyan', icon: Clapperboard, tab: '1. Screenplay & Lore' },
    { name: 'Visual Studio', detail: 'layered SVGs & 3D turnarounds (Module 2)', color: 'violet', icon: Layers3, tab: '2. Visual & 3D Art' },
    { name: 'Audio Studio', detail: 'adaptive stems & zero-shot Foley (Module 3)', color: 'amber', icon: AudioLines, tab: '3. Audio & Soundscapes' },
    { name: 'Creator Agent', detail: 'reels & thumbnail heatmaps (Module 4)', color: 'pink', icon: Radio, tab: '4. Distribution Hub' },
  ]
  return (
    <main className="landing-shell">
      <header className="landing-header">
        <button className="landing-brand" aria-label="DirectR home">
          <span className="landing-brand-icon"><Clapperboard size={18} /></span>
          <span className="landing-brand-name">Direct<span>R</span><small>AUTONOMOUS CREATIVE STUDIO</small></span>
        </button>
        <div className="landing-header-right">
          <span className="landing-agent-chip"><i /> MULTI-AGENT SWARM</span>
          <span className="local-chip"><i /> LIVE MVP READY</span>
        </div>
      </header>
      <section className="landing-hero">
        <div className="landing-copy">
          <span className="landing-kicker"><Sparkles size={13} /> YOUR CREATIVE SWARM, IN SYNC</span>
          <h1>From first prompt<br />to <span>production cut.</span></h1>
          <p className="landing-description">DirectR unifies narrative screenwriting, controllable vector art turnarounds, and adaptive audio soundscapes into a synchronized multi-agent pipeline.</p>
          <button className="landing-cta" onClick={() => onEnter()}><Zap size={16} fill="currentColor" /> Enter the studio <ArrowRight size={16} /></button>
          <div className="landing-proof">
            <span><i /> Module 1: Screenplay & Dialogue</span>
            <span><Activity size={13} /> Module 2: Layered SVG & Turnarounds</span>
            <span><Database size={13} /> Module 3: Tension Audio Mix</span>
          </div>
        </div>
        <div className="landing-visual">
          <div className="signal-card">
            <div className="signal-heading"><span><Activity size={15} /> Swarm Signal</span><b><i /> LIVE</b></div>
            <div className="chart-area">
              <div className="chart-gridline" />
              <div className="chart-bars">{bars.map((height, i) => <i key={i} className={`bar bar-${i % 4}`} style={{height: `${height}%`}} />)}</div>
              <div className="chart-axis"><span>MODULE 01</span><span>MODULE 02</span><span>MODULE 03</span></div>
            </div>
            <div className="signal-foot"><span>CHRONICLES OF NEO-AETHEL</span><strong>LIVE <small>SYNCED</small></strong></div>
          </div>
          <div className="agent-mesh">
            <div className="mesh-heading"><span>THE DIRECTR PIPELINE</span><span className="mesh-line" /><small>FOUR SPECIALIST TRACKS</small></div>
            <div className="agent-grid">
              {agents.map(({ name, detail, color, icon: Icon, tab }, i) => (
                <button key={name} type="button" onClick={() => onEnter(tab)} aria-label={`Open ${name}`} className={`agent-tile ${color} float-${i + 1} ${i === 0 || i === 1 ? 'agent-featured' : ''}`}>
                  <div className="agent-tile-top"><Icon size={17} /><span className="agent-status"><i /> READY</span></div>
                  <strong>{name}</strong>
                  <small>{detail}</small>
                  <span className="agent-open-hint">LAUNCH MODULE <ArrowRight size={10} /></span>
                </button>
              ))}
            </div>
            <div className="mesh-footer"><span><i /> UNIFIED PYDANTIC SCHEMAS</span><span>CORE ENGINE <ArrowRight size={12} /></span></div>
          </div>
          <div className="orbit orbit-one" /><div className="orbit orbit-two" />
        </div>
      </section>
      <footer className="landing-footer">
        <span>DirectR — Autonomous Multi-Agent AI Creative Production Studio.</span>
        <span>MODULE 1 (NARRATIVE) <b>·</b> MODULE 2 (VISUAL) <b>·</b> MODULE 3 (AUDIO) <b>·</b> MODULE 4 (CREATOR)</span>
      </footer>
    </main>
  )
}

function CreativeHome({ onOpenStudio, prompt, setPrompt, onRunBrief }: { onOpenStudio: () => void; prompt: string; setPrompt: (v: string) => void; onRunBrief: (customPrompt: string) => void }) {
  const [category, setCategory] = useState('Cyberpunk Sci-Fi')
  const categories = ['Cyberpunk Sci-Fi', 'Dystopian Noir', 'Space Opera', 'Dark Fantasy']

  return (
    <main className="home-shell">
      <aside className="home-sidebar">
        <button className="home-back" aria-label="Back to DirectR landing">
          <span className="landing-brand-icon"><Clapperboard size={17} /></span>
          <span className="landing-brand-name">Direct<span>R</span><small>CREATIVE STUDIO</small></span>
        </button>
        <button className="new-project" onClick={onOpenStudio}><Plus size={15} /> New production <span>⌘ N</span></button>
        <div className="home-side-label">WORKSPACE</div>
        <button className="home-nav active"><Gauge size={15} /> Home</button>
        <button className="home-nav" onClick={onOpenStudio}><Clapperboard size={15} /> Full Studio <ArrowRight size={13} /></button>
        <button className="home-nav" onClick={onOpenStudio}><FolderOpen size={15} /> Projects <span>03</span></button>
        <div className="home-side-label recent-label">ACTIVE PRODUCTIONS <button aria-label="Search projects"><Search size={12} /></button></div>
        <button className="recent-project active-project" onClick={onOpenStudio}>
          <span className="project-thumb"><img src="/lyra-neon.png" alt="" /></span>
          <span><strong>Chronicles of Neo-Aethel</strong><small>Active · 3 scenes</small></span>
          <i />
        </button>
        <button className="recent-project" onClick={onOpenStudio}>
          <span className="project-thumb second-thumb"><Film size={14} /></span>
          <span><strong>The Cipher Protocol</strong><small>Draft · Dialect test</small></span>
        </button>
        <button className="recent-project" onClick={onOpenStudio}>
          <span className="project-thumb third-thumb"><AudioLines size={14} /></span>
          <span><strong>District 09 Slums</strong><small>24-EDO Soundscape</small></span>
        </button>
        <div className="sidebar-bottom">
          <div className="home-agent-status">
            <span><Activity size={14} /></span>
            <div><strong>Backend Synced</strong><small>Module 1 & 2 Active</small></div>
            <i />
          </div>
          <div className="home-profile">
            <div className="profile-orb">DR</div>
            <span><strong>Creative Director</strong><small>STUDIO LEAD</small></span>
            <MoreHorizontal size={16} />
          </div>
        </div>
      </aside>
      <section className="home-main">
        <header className="home-topbar">
          <div className="home-crumb">WORKSPACE <ChevronRight size={11} /> <strong>CREATIVE BRIEF INPUT</strong></div>
          <div className="home-top-actions">
            <span className="home-runtime"><i /> PIPELINE READY</span>
            <button className="home-studio-link" onClick={onOpenStudio}><Activity size={14} /> Open full studio <ArrowRight size={13} /></button>
          </div>
        </header>
        <div className="home-content">
          <div className="home-welcome">
            <span className="landing-kicker"><Sparkles size={13} /> SYNTHESIZE PRODUCTION FROM BRIEF</span>
            <h1>Enter your logline.<br /><span>Direct the swarm.</span></h1>
            <p>Input your creative concept below. The swarm will immediately generate character constraints, dialect-adaptive screenplay beats, layered vector SVGs, and adaptive audio stems.</p>
          </div>
          <div className="prompt-composer">
            <div className="prompt-topline">
              <span><WandSparkles size={14} /> LIVE PRODUCTION BRIEF INPUT</span>
              <span className="prompt-context"><i /> AGENT SWARM ROUTED</span>
            </div>
            <label className="sr-only" htmlFor="creative-prompt">Describe your creative brief</label>
            <textarea
              id="creative-prompt"
              value={prompt}
              onChange={e => setPrompt(e.target.value)}
              placeholder="e.g. In a submerged neon metropolis, a lone archivist and a rogue pilot uncover a sentient AI code that alters physical architecture..."
              rows={3}
            />
            <div className="prompt-controls">
              <button
                className="prompt-attach"
                onClick={() => setPrompt("In the rain-slicked underground sectors of Neo-Aethel, Lyra Vance discovers a corrupted memory shard containing the blueprint of the city's sunken archives.")}
                title="Load Preset Cyberpunk Concept"
              >
                <Plus size={16} />
              </button>
              <span className="prompt-hint">Module 1 (Screenplay) & Module 2 (Visuals) will execute on this brief</span>
              <button className="prompt-quality" onClick={() => setCategory(categories[(categories.indexOf(category) + 1) % categories.length])}>
                GENRE: {category.toUpperCase()} <ChevronDown size={12} />
              </button>
              <button className="prompt-submit" onClick={() => onRunBrief(prompt)} aria-label="Synthesize Full Production Package">
                <ArrowRight size={16} />
              </button>
            </div>
          </div>
          <div className="home-category-row">
            {categories.map((item, i) => (
              <button key={item} className={category === item ? 'home-category selected' : 'home-category'} onClick={() => setCategory(item)}>
                {[<Film key="film" size={12} />, <Sparkles key="spark" size={12} />, <AudioLines key="audio" size={12} />, <Radio key="radio" size={12} />][i]}
                {item}
              </button>
            ))}
          </div>
          <div className="home-section-head">
            <div>
              <span className="eyebrow">READY FOR SYNTHESIS</span>
              <h2>Active Production Setup</h2>
            </div>
            <button onClick={onOpenStudio}>Go to Studio Workspace <ArrowRight size={13} /></button>
          </div>
          <div className="home-project-grid">
            <button className="home-project-card featured-project" onClick={onOpenStudio}>
              <div className="home-project-art">
                <img src="/lyra-neon.png" alt="Lyra Vance concept art" />
                <span className="project-live"><i /> MODULE 1 & 2 READY</span>
                <span className="project-open"><Play size={13} fill="currentColor" /></span>
              </div>
              <div className="home-project-info">
                <div>
                  <strong>Chronicles of Neo-Aethel</strong>
                  <small>Cyberpunk sci-fi fantasy · 3 scenes generated</small>
                </div>
                <span className="project-progress">100%</span>
              </div>
              <div className="home-progress"><i /></div>
            </button>
            <button className="home-project-card compact-project" onClick={onOpenStudio}>
              <div className="mini-wave">
                <span /><span /><span /><span /><span /><span /><span /><span />
                <span /><span /><span /><span /><span /><span /><span /><span />
              </div>
              <span className="project-live"><i /> MODULE 3</span>
              <div className="compact-info">
                <AudioLines size={16} />
                <span><strong>Adaptive Stem Engine</strong><small>24-EDO Harmony & Foley</small></span>
                <ArrowRight size={14} />
              </div>
            </button>
            <button className="home-project-card start-card" onClick={onOpenStudio}>
              <span className="start-orb"><Plus size={20} /></span>
              <strong>Open Multi-Panel View</strong>
              <small>Real-time parameter manipulation</small>
              <span className="start-arrow"><ArrowRight size={14} /></span>
            </button>
          </div>
          <div className="home-footer">
            <span><Activity size={12} /> DYNAMIC RE-SYNTHESIS READY</span>
            <span>PYTHON BACKEND CONNECTED <i /></span>
          </div>
        </div>
      </section>
    </main>
  )
}

export default function DirectRStudio() {
  const [view, setView] = useState<'landing' | 'home' | 'studio'>('landing')
  const [tension, setTension] = useState(.72)
  const [scene, setScene] = useState(1)
  const [tab, setTab] = useState<Tab>('Full Studio View')
  const [running, setRunning] = useState(false)
  const [step, setStep] = useState(0)
  const [npcModal, setNpcModal] = useState(false)
  const [npcLoading, setNpcLoading] = useState(false)

  // Project brief input state
  const [prompt, setPrompt] = useState('In a submerged neon metropolis, a lone archivist and a rogue pilot uncover a sentient AI code that alters physical architecture.')
  const [projectTitle, setProjectTitle] = useState('Chronicles of Neo-Aethel')
  const [projectGenre, setProjectGenre] = useState('Cyberpunk Sci-Fi Fantasy')

  // Real backend live data state
  const [backendConnected, setBackendConnected] = useState(false)
  const [backendScenes, setBackendScenes] = useState<any[]>([])
  const [activeStems, setActiveStems] = useState<string[]>([])
  const [liveBpm, setLiveBpm] = useState<number>(126)
  const [foleyList, setFoleyList] = useState<any[]>([])
  const [generatedNpc, setGeneratedNpc] = useState<any>(null)

  // Module 2 Visual states
  const [svgMarkup, setSvgMarkup] = useState<string>('')
  const [anchorCount, setAnchorCount] = useState<number>(16)
  const [turnaroundPrompt, setTurnaroundPrompt] = useState<string>('')

  // Initial check & data fetch from Python backend API
  useEffect(() => {
    async function checkBackend() {
      try {
        const res = await fetch('/api/status')
        if (res.ok) {
          const data = await res.json()
          setBackendConnected(true)
          fetchNarrative()
          fetchVisuals()
        }
      } catch (err) {
        console.log('DirectR Backend API offline, running in preview mode.')
      }
    }
    checkBackend()
  }, [])

  // Sync tension to Audio Backend
  useEffect(() => {
    setScene(tension > .78 ? 2 : tension > .4 ? 1 : 0)

    async function syncAudio() {
      try {
        const res = await fetch('/api/audio/arrange', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ tension })
        })
        if (res.ok) {
          const data = await res.json()
          setActiveStems(data.active_stems || [])
          setLiveBpm(data.bpm || Math.round(65 + tension * 85))
          if (data.foley_cues) setFoleyList(data.foley_cues)
        }
      } catch (e) {
        setLiveBpm(Math.round(65 + tension * 85))
      }
    }
    syncAudio()
  }, [tension])

  async function fetchNarrative(customBrief?: any) {
    try {
      const res = await fetch('/api/narrative/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: customBrief?.title || projectTitle,
          genre: customBrief?.genre || projectGenre,
          logline: customBrief?.logline || prompt,
        })
      })
      if (res.ok) {
        const data = await res.json()
        if (data.scenes && data.scenes.length > 0) {
          setBackendScenes(data.scenes)
        }
      }
    } catch (e) {
      console.log('Could not fetch narrative from backend, using defaults.')
    }
  }

  async function fetchVisuals(sceneNum?: number) {
    try {
      const res = await fetch('/api/visual/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: `${projectTitle}: Scene ${sceneNum || scene + 1}`,
          scene_number: sceneNum || scene + 1,
          character_name: 'Lyra Vance',
          character_archetype: 'Sub-surface Archivist',
        })
      })
      if (res.ok) {
        const data = await res.json()
        setSvgMarkup(data.svg_markup || '')
        setAnchorCount(data.anchor_nodes_count || 16)
        if (data.turnaround?.prompt) {
          setTurnaroundPrompt(data.turnaround.prompt)
        }
      }
    } catch (e) {
      console.log('Could not fetch visual assets from backend.')
    }
  }

  async function handleGenerateNpc() {
    setNpcLoading(true)
    setNpcModal(true)
    try {
      const res = await fetch('/api/narrative/npc', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: 'Iona "Switch" Marrow',
          relationship: 'Reluctant Informant / Memory Broker',
          setting: 'District 9 Lower Slums',
          use_llm: true
        })
      })
      if (res.ok) {
        const data = await res.json()
        setGeneratedNpc(data.npc)
      } else {
        setGeneratedNpc(null)
      }
    } catch (e) {
      setGeneratedNpc(null)
    } finally {
      setNpcLoading(false)
    }
  }

  function handleRunBrief(customPrompt: string) {
    setPrompt(customPrompt)
    fetchNarrative({ logline: customPrompt })
    fetchVisuals(1)
    setTab('Full Studio View')
    setView('studio')
    startRun()
  }

  useEffect(() => {
    if (!running || step >= 4) return
    const timer = window.setTimeout(() => setStep(v => v + 1), 1050)
    return () => window.clearTimeout(timer)
  }, [running, step])

  const visible = (module: string) => tab === 'Full Studio View' || tab === module

  function exportPackage() {
    const data = {
      project: projectTitle,
      genre: projectGenre,
      durationMinutes: 5,
      scenes: backendScenes.length > 0 ? backendScenes : defaultScenes,
      characters: ['Lyra Vance', 'Kaelen Cross'],
      dramaticTension: tension,
      tempoBpm: liveBpm,
      activeStems: activeStems.length > 0 ? activeStems : defaultStems,
      visualAnchorNodes: anchorCount,
      generatedAt: new Date().toISOString()
    }
    const link = document.createElement('a')
    link.href = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' }))
    link.download = `directr-${projectTitle.toLowerCase().replace(/\\s+/g, '-')}-production.json`
    link.click()
    URL.revokeObjectURL(link.href)
  }

  function startRun() {
    setStep(0)
    setRunning(true)
    fetchNarrative()
    fetchVisuals()
  }

  if (view === 'landing') {
    return (
      <LandingPage
        onEnter={(destination) => {
          if (destination) {
            setTab(destination)
            setView('studio')
          } else {
            setView('home')
          }
        }}
      />
    )
  }

  if (view === 'home') {
    return (
      <CreativeHome
        onOpenStudio={() => {
          setTab('Full Studio View')
          setView('studio')
        }}
        prompt={prompt}
        setPrompt={setPrompt}
        onRunBrief={handleRunBrief}
      />
    )
  }

  return (
    <main className="studio-shell">
      <Header
        tension={tension}
        setTension={setTension}
        onRun={startRun}
        onExport={exportPackage}
        backendConnected={backendConnected}
        projectTitle={projectTitle}
        projectGenre={projectGenre}
      />
      <div className="workspace">
        <nav className="studio-nav" aria-label="Studio modules">
          <div className="workspace-label"><span>WORKSPACE</span><button title="Studio help" aria-label="Studio help"><CircleHelp size={15} /></button></div>
          <button className="nav-tab home-return" onClick={() => setView('home')}><span className="nav-index"><House size={14} /></span>Home Brief<ChevronRight size={13} /></button>
          <div className="tab-row">{tabs.map((item, i) => <button key={item} onClick={() => setTab(item)} className={tab === item ? 'nav-tab current' : 'nav-tab'}><span className="nav-index">{i === 0 ? <Gauge size={14} /> : `0${i}`}</span>{item}<ChevronRight size={13} /></button>)}</div>
          <div className="nav-bottom">
            <div className="swarm-card">
              <span className="swarm-orb"><Activity size={16} /></span>
              <div><strong>{backendConnected ? 'Backend Connected' : 'Swarm Standby'}</strong><small>{backendConnected ? 'Modules 1, 2, 3 Active' : 'Run api_server.py'}</small></div>
              <i />
            </div>
            <div className="operator"><div className="operator-avatar">DR</div><div><strong>Studio Operator</strong><small>CREATIVE DIRECTOR</small></div><MoreHorizontal size={16} /></div>
          </div>
        </nav>
        <div className="studio-content">
          <div className="content-heading">
            <div>
              <div className="breadcrumb">PROJECTS <ChevronRight size={11} /> {projectTitle.toUpperCase()} <ChevronRight size={11} /> <b>{tab === 'Full Studio View' ? 'FULL STUDIO' : tab.split('. ')[1]?.toUpperCase()}</b></div>
              <h1>{tab === 'Full Studio View' ? 'Production overview' : tab.split('. ')[1] || tab}<span className="live-label"><i /> {backendConnected ? 'MODULE 1 & 2 LIVE' : 'DEMO PREVIEW'}</span></h1>
            </div>
            <div className="content-tools">
              <button title="Refresh All Modules" aria-label="Refresh All Modules" onClick={() => { fetchNarrative(); fetchVisuals(); }}><RefreshCw size={15} /></button>
              <button title="Audio monitoring" aria-label="Audio monitoring"><Headphones size={15} /></button>
              <span className="date-label">LIVE SYNCHRONIZATION ACTIVE</span>
            </div>
          </div>
          <div className="metric-strip">
            <div><span><Film size={13} /> SEQUENCE</span><strong>03 <small>SCENES</small></strong></div>
            <div><span><Mic2 size={13} /> CAST</span><strong>02 <small>CHARACTERS</small></strong></div>
            <div><span><Layers3 size={13} /> VECTOR NODES</span><strong>{anchorCount} <small>ANCHORS</small></strong></div>
            <div><span><Music2 size={13} /> SCORE TEMPO</span><strong>{liveBpm} <small>BPM</small></strong></div>
            <div><span><SlidersHorizontal size={13} /> TENSION</span><strong>{tension.toFixed(2)} <small>/ 1.00</small></strong></div>
            <div className="metric-status" style={{ color: backendConnected ? '#10b981' : undefined }}>
              <i style={{ background: backendConnected ? '#10b981' : undefined }} /> {backendConnected ? 'MODULES 1 & 2 & 3 INTEGRATED' : 'LOCAL SERVER STANDBY'}
            </div>
          </div>
          <div className={`panels-grid ${tab === 'Full Studio View' ? '' : 'single-view'}`}>
            {visible('1. Screenplay & Lore') && (
              <NarrativePanel
                scene={scene}
                setScene={(s) => { setScene(s); fetchVisuals(s + 1); }}
                onNpc={handleGenerateNpc}
                backendScenes={backendScenes}
                loading={npcLoading}
              />
            )}
            {visible('2. Visual & 3D Art') && (
              <VisualPanel
                tension={tension}
                svgMarkup={svgMarkup}
                anchorCount={anchorCount}
                turnaroundPrompt={turnaroundPrompt}
              />
            )}
            {visible('3. Audio & Soundscapes') && (
              <AudioPanel
                tension={tension}
                activeStems={activeStems}
                liveBpm={liveBpm}
                foleyList={foleyList}
              />
            )}
            {visible('4. Distribution Hub') && <CreatorPanel />}
          </div>
          <footer className="status-footer">
            <span><i /> {backendConnected ? 'DirectR Python Backend Running (Port 8000)' : 'Running Standalone Client'}</span>
            <span><Activity size={11} /> AUTOSAVE ON</span>
            <span>DIRECTR STUDIO <b>v1.08.4 MVP</b></span>
          </footer>
        </div>
      </div>
      {running && <RunModal step={step} onClose={() => setRunning(false)} />}
      {npcModal && (
        <div className="modal-backdrop" role="presentation" onClick={() => setNpcModal(false)}>
          <section className="npc-modal" role="dialog" aria-modal="true" aria-labelledby="npc-title" onClick={e => e.stopPropagation()}>
            <div className="modal-top">
              <div className="modal-icon"><Sparkles size={17} /></div>
              <button className="icon-button" aria-label="Close NPC details" onClick={() => setNpcModal(false)}>×</button>
            </div>
            <div className="eyebrow">MODULE 1 / REACTIVE NPC BACKSTORY (NVIDIA NEMOTRON)</div>
            <h2 id="npc-title">{generatedNpc?.name || 'Iona “Switch” Marrow'}</h2>
            <p className="modal-copy">
              {generatedNpc?.relationship ? `${generatedNpc.relationship} in ${generatedNpc.origin_setting || 'District 9 Lower Slums'}` : 'A signal broker who sells memories by the minute—and recognizes Lyra from a life she doesn’t remember.'}
            </p>
            <div className="npc-facts">
              <div>
                <span>FACTION</span>
                <strong>{generatedNpc?.faction || 'The Unmoored'}</strong>
              </div>
              <div>
                <span>SECRET MOTIVE</span>
                <strong>{generatedNpc?.secret_motivation || 'Recover her erased identity'}</strong>
              </div>
              <div>
                <span>ALLEGIANCE</span>
                <strong>{generatedNpc?.allegiance_level ? `${(generatedNpc.allegiance_level * 100).toFixed(0)}%` : '85%'}</strong>
              </div>
            </div>
            {generatedNpc?.memory_tree_nodes && generatedNpc.memory_tree_nodes.length > 0 && (
              <div style={{ marginTop: '16px', background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.08)' }}>
                <div style={{ fontSize: '11px', color: '#6ee7b7', fontWeight: 600, marginBottom: '6px' }}>VECTOR MEMORY TREE NODE:</div>
                <div style={{ fontSize: '13px', color: '#cbd5e1', lineHeight: '1.4' }}>{generatedNpc.memory_tree_nodes[0]}</div>
              </div>
            )}
            <button className="modal-done" onClick={() => setNpcModal(false)}>Add to LoreBible <Check size={14} /></button>
          </section>
        </div>
      )}
    </main>
  )
}
