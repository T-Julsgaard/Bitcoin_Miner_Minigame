import os

# --- CONFIGURATION ---
# WE USE THE EXACT ABSOLUTE PATH YOU PROVIDED
TARGET_DIR = r"C:\Users\thoma\Desktop\Bitcoin_Miner_Minigame\output"
FILE_NAME = "index.html"

# 1. Create the directory if it doesn't exist
if not os.path.exists(TARGET_DIR):
    try:
        os.makedirs(TARGET_DIR)
        print(f"✅ Created folder: {TARGET_DIR}")
    except OSError as e:
        print(f"❌ Error creating directory: {e}")
        # Stop here if we can't create the folder
        exit()

# 2. Define the full file path
OUTPUT_FILE = os.path.join(TARGET_DIR, FILE_NAME)

# --- THE GAME CODE (v21 Final) ---
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bitcoin Miner</title>
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='50' fill='%23F7931A'/%3E%3Cpath fill='%23FFF' d='M73.6 42.1c1.8-12-7.4-15.6-18.7-16.7l3.2-12.8-7.8-2-3.1 12.5c-2-.5-4.1-1-6.1-1.5l3.2-12.6-7.8-2-3.2 12.7c-1.7-.4-3.3-.8-4.9-1.2l.1-.3-10.8-2.7-2.1 8.4s5.8 1.3 5.7 1.4c3.2.8 3.8 2.9 3.7 4.5l-3.7 14.9c.2 0 .5.1.8.2l-4.1 16.3c-.3 2.1-1.1 5.3-4.2 4.5.1.1-5.7-1.4-5.7-1.4l-4 9.1 10.1 2.5c1.9.5 3.7 1 5.5 1.4l-3.2 13 7.8 1.9 3.2-12.8c2.1.6 4.1 1.1 6.1 1.6l-3.2 12.9 7.8 1.9 3.3-13.1c13.3 2.5 23.3 1.5 27.5-10.5 3.4-9.6-.2-15.1-7-18.8 5-1.1 8.7-4.4 9.7-11zm-13.2 18.5c-1.8 7.2-14 3.3-17.9 2.4l3.2-12.8c3.9 1 16.3 2.8 14.7 10.4zm1.8-18.6c-1.6 6.6-11.5 3.2-14.7 2.4l2.9-11.6c3.2.8 13.3 2.3 11.8 9.2z'/%3E%3C/svg%3E">
    <style>
        /* --- GLOBAL THEME --- */
        :root {
            --bg-color: #080808;
            --panel-bg: rgba(20, 20, 20, 0.95);
            --border-color: #333;
            --highlight: #F7931A; /* Bitcoin Orange */
            --highlight-dim: #945d1d;
            --text-primary: #f0f0f0;
            --text-secondary: #888;
            --font-main: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            --font-mono: 'Courier New', monospace;
        }

        body { 
            margin: 0; 
            overflow: hidden; 
            background: var(--bg-color); 
            font-family: var(--font-main); 
            user-select: none; 
            -webkit-font-smoothing: antialiased;
            
            /* GLOBAL CUSTOM CURSOR (Orange Arrow) */
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath d='M2 2l0 18l5-5l5 7l3-3l-6-6l6 0z' fill='%23F7931A' stroke='%23000' stroke-width='1.5'/%3E%3C/svg%3E"), auto;
        }

        /* Enforce custom cursor on buttons */
        button, .interactive {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath d='M2 2l0 18l5-5l5 7l3-3l-6-6l6 0z' fill='%23F7931A' stroke='%23000' stroke-width='1.5'/%3E%3C/svg%3E"), pointer !important;
        }

        /* HIDE CURSOR IN-GAME */
        body.gaming {
            cursor: none !important;
        }
        body.gaming button {
            cursor: none !important; 
        }

        /* --- GAME CURSOR (RETICLE) --- */
        #cursor-container {
            position: fixed; top: 0; left: 0; pointer-events: none; z-index: 9999;
            transform: translate(-50%, -50%);
            display: none; 
        }
        
        body.gaming #cursor-container { display: block; }

        #aim-reticle {
            width: 30px; height: 30px;
            border: 2px solid rgba(255, 255, 255, 0.9);
            border-radius: 50%;
            box-sizing: border-box;
            box-shadow: 0 0 4px rgba(0,0,0,0.5);
            transition: transform 0.1s ease-out;
        }

        /* Click Animation (Pulse) */
        .click-pulse {
            animation: pulseClick 0.2s ease-out forwards;
        }

        @keyframes pulseClick {
            0% { transform: scale(1); border-color: #fff; }
            50% { transform: scale(1.4); border-color: var(--highlight); border-width: 3px; }
            100% { transform: scale(1); border-color: rgba(255, 255, 255, 0.9); }
        }

        /* --- UI COMPONENTS --- */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #111; }
        ::-webkit-scrollbar-thumb { background: #444; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--highlight); }

        #canvas-wrapper { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
        #ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; }
        .interactive { pointer-events: auto; }

        /* HUD */
        #hud-top {
            position: absolute; top: 0; left: 0; width: 100%; height: 100px;
            background: linear-gradient(to bottom, rgba(0,0,0,0.9), transparent);
            display: flex; justify-content: space-between; align-items: flex-start;
            padding: 30px 50px; box-sizing: border-box;
            display: none;
        }

        .hud-group { display: flex; flex-direction: column; }
        .hud-left { align-items: flex-start; }
        .hud-right { align-items: flex-end; }

        .hud-value { 
            font-family: var(--font-mono); font-size: 54px; font-weight: 700; color: #fff; 
            text-shadow: 0 0 20px rgba(255,255,255,0.1); line-height: 1;
        }
        .hud-value.orange { color: var(--highlight); text-shadow: 0 0 20px rgba(247, 147, 26, 0.4); }
        
        .hud-label { 
            font-size: 11px; letter-spacing: 2px; color: var(--text-secondary); 
            margin-top: 5px; text-transform: uppercase; font-weight: 600;
        }

        /* Live Feed */
        #feed-widget {
            position: absolute; bottom: 30px; right: 30px;
            width: 280px; text-align: right;
            display: flex; flex-direction: column; gap: 6px;
            display: none;
        }
        .feed-header {
            font-size: 10px; letter-spacing: 1.5px; color: var(--text-secondary);
            border-bottom: 1px solid var(--border-color); padding-bottom: 4px; margin-bottom: 4px;
        }
        .feed-row {
            font-family: var(--font-mono); font-size: 12px; color: var(--text-secondary);
            opacity: 0; animation: slideIn 0.3s forwards;
        }
        .feed-amt { color: var(--highlight); font-weight: bold; margin-left: 8px; }
        @keyframes slideIn { from { opacity: 0; transform: translateX(10px); } to { opacity: 1; transform: translateX(0); } }

        /* SCREENS */
        .screen-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(5, 5, 5, 0.96); z-index: 20;
            display: none; flex-direction: column; align-items: center; justify-content: center;
        }
        .screen-overlay.active { display: flex; }

        h1 { 
            font-size: 48px; color: var(--highlight); margin: 0 0 20px 0; letter-spacing: 8px; font-weight: 800;
            border-bottom: 3px solid var(--highlight); padding-bottom: 15px; text-transform: uppercase;
        }
        
        /* UNIFIED MENU TEXT */
        .menu-text-group { 
            text-align: center; margin-bottom: 40px; display: flex; flex-direction: column; gap: 8px;
        }
        .menu-line {
            font-size: 14px; color: var(--text-secondary); letter-spacing: 1.5px; text-transform: uppercase; font-weight: 600;
        }
        .menu-line span { color: #fff; }

        /* BUTTONS */
        .btn-row { display: flex; gap: 20px; margin-top: 10px; }
        
        button {
            background: var(--highlight); color: #000; border: none;
            padding: 16px 40px; font-size: 16px; font-weight: 700; letter-spacing: 1px;
            cursor: pointer; transition: all 0.2s ease; border-radius: 4px; min-width: 180px;
        }
        button:hover { background: #ffaa33; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(247, 147, 26, 0.3); }
        button:active { transform: translateY(0); }

        button.secondary {
            background: transparent; color: var(--highlight); border: 2px solid var(--highlight);
        }
        button.secondary:hover { background: rgba(247, 147, 26, 0.1); }

        /* DATA TABLES */
        .data-panel {
            width: 80%; max-width: 900px; background: var(--panel-bg);
            border: 1px solid var(--border-color); border-radius: 6px;
            display: flex; flex-direction: column; overflow: hidden;
        }
        .panel-header {
            display: flex; justify-content: space-between; padding: 15px 20px;
            background: #151515; border-bottom: 1px solid var(--border-color);
            font-size: 11px; font-weight: 700; color: var(--text-secondary); letter-spacing: 1px;
        }
        .panel-body { max-height: 40vh; overflow-y: auto; }
        
        .data-row {
            display: flex; justify-content: space-between; padding: 12px 20px;
            border-bottom: 1px solid #222; font-family: var(--font-mono); font-size: 13px; color: #aaa;
            transition: background 0.1s;
        }
        .data-row:hover { background: #1a1a1a; }
        .data-row:last-child { border-bottom: none; }
        
        .col-hash { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-right: 20px; color: #666; }
        .col-val { min-width: 100px; text-align: right; color: var(--highlight); font-weight: bold; }
        
        .stats-grid { display: flex; gap: 60px; margin-bottom: 30px; }
        .stat-item { text-align: center; }
        .stat-num { font-size: 36px; font-weight: 700; color: #fff; display: block; margin-bottom: 5px; }
        .stat-name { font-size: 11px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px; }

        /* POP EFFECT */
        .pop-float {
            position: absolute; font-size: 24px; font-weight: 900; color: #fff;
            pointer-events: none; text-shadow: 0 0 10px var(--highlight);
            animation: popUp 0.6s cubic-bezier(0.18, 0.89, 0.32, 1.28) forwards; z-index: 100;
        }
        @keyframes popUp {
            0% { transform: translate(-50%, 0) scale(0.5); opacity: 0; }
            40% { transform: translate(-50%, -30px) scale(1.4); opacity: 1; }
            100% { transform: translate(-50%, -80px) scale(1.0); opacity: 0; }
        }
        
        .hidden { display: none !important; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="canvas-wrapper"></div>
    
    <div id="cursor-container">
        <div id="aim-reticle"></div>
    </div>

    <div id="ui-layer">
        
        <div id="hud-top">
            <div class="hud-group hud-left">
                <div id="timer-display" class="hud-value">30.00</div>
                <div class="hud-label">TIME REMAINING</div>
            </div>
            <div class="hud-group hud-right">
                <div id="score-display" class="hud-value orange">0.00000000</div>
                <div class="hud-label">MINED BTC</div>
            </div>
        </div>

        <div id="feed-widget">
            <div id="feed-list"></div>
            <div class="feed-header">LIVE NODE FEED</div>
        </div>

        <div id="screen-menu" class="screen-overlay active interactive">
            <h1>BITCOIN MINER</h1>
            <div class="menu-text-group">
                <div class="menu-line">CLICK TRANSACTIONS TO MINE BITCOIN</div>
                <div class="menu-line">LIVE ON-CHAIN TRANSACTION DATA</div>
                <div class="menu-line">CURRENT BLOCK HEIGHT: <span id="menu-block">Loading...</span></div>
            </div>
            <div class="btn-row">
                <button onclick="Game.start()">START MINING</button>
                <button class="secondary" onclick="UI.showScreen('screen-leaderboard')">LEADERBOARD</button>
            </div>
        </div>

        <div id="screen-gameover" class="screen-overlay interactive">
            <h1 style="border:none; color:#fff; font-size:36px">SESSION REPORT</h1>
            <div class="stats-grid">
                <div class="stat-item">
                    <span id="end-score" class="stat-num" style="color:var(--highlight)">0.00</span>
                    <span class="stat-name">TOTAL MINED</span>
                </div>
                <div class="stat-item">
                    <span id="end-missed" class="stat-num" style="color:#444">0.00</span>
                    <span class="stat-name">MISSED</span>
                </div>
            </div>
            <div class="data-panel">
                <div class="panel-header">
                    <span>TRANSACTION ID</span>
                    <span>BTC VALUE</span>
                </div>
                <div id="log-list" class="panel-body"></div>
            </div>
            <div class="btn-row">
                <button onclick="Game.start()">PLAY AGAIN</button>
                <button class="secondary" onclick="UI.showScreen('screen-menu')">MENU</button>
            </div>
        </div>

        <div id="screen-leaderboard" class="screen-overlay interactive">
            <h1>HIGH SCORES</h1>
            <div class="data-panel" style="height: 50%;">
                <div class="panel-header">
                    <span>RANK / BLOCK</span>
                    <span>SCORE</span>
                </div>
                <div id="leaderboard-list" class="panel-body"></div>
            </div>
            <div class="btn-row">
                <button class="secondary" onclick="UI.showScreen('screen-menu')">BACK</button>
            </div>
        </div>

        <div id="screen-modal" class="screen-overlay interactive" style="background:rgba(0,0,0,0.98)">
            <h1 style="font-size:32px; border:none">TRANSACTION LOG</h1>
            <div class="data-panel">
                <div class="panel-header">
                    <span>TRANSACTION ID</span>
                    <span>BTC VALUE</span>
                </div>
                <div id="modal-list" class="panel-body"></div>
            </div>
            <div class="btn-row">
                <button class="secondary" onclick="UI.showScreen('screen-leaderboard')">CLOSE</button>
            </div>
        </div>

    </div>

    <script>
        /**
         * BITCOIN MINER - Standalone Final v21
         */
        
        const CONFIG = {
            duration: 30,
            spawnRange: 35,
            spawnHeight: 45,
            colors: {
                pale: new THREE.Color("#885500"),
                mid:  new THREE.Color("#fb8c00"),
                deep: new THREE.Color("#ffaa00"),
                super: new THREE.Color("#ff0000") 
            }
        };

        class GameManager {
            constructor() {
                this.score = 0;
                this.timeLeft = CONFIG.duration;
                this.isPlaying = false;
                this.currentBlock = "---";
                this.cubes = [];
                this.hitboxes = [];
                this.sessionTxs = [];       
                this.lootedHashes = new Set();
                
                this.initThreeJS();
                this.initEvents();
                this.fetchBlockData();
                this.connectNetwork();
            }

            initThreeJS() {
                this.scene = new THREE.Scene();
                this.scene.background = new THREE.Color(0x050505);
                this.scene.fog = new THREE.Fog(0x050505, 40, 120);

                this.camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
                this.camera.position.set(0, 20, 60);
                this.camera.lookAt(0, 5, 0);

                this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
                this.renderer.setSize(window.innerWidth, window.innerHeight);
                this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
                document.getElementById('canvas-wrapper').appendChild(this.renderer.domElement);

                const ambient = new THREE.AmbientLight(0xffffff, 0.6);
                const pLight = new THREE.PointLight(0xF7931A, 2, 100);
                pLight.position.set(0, 20, 10);
                this.scene.add(ambient, pLight);

                const floorGeo = new THREE.PlaneGeometry(500, 500);
                const floorMat = new THREE.MeshBasicMaterial({ color: 0x080808 });
                const floor = new THREE.Mesh(floorGeo, floorMat);
                floor.rotation.x = -Math.PI / 2;
                floor.position.y = -60; 
                this.scene.add(floor);

                this.raycaster = new THREE.Raycaster();
                this.mouse = new THREE.Vector2();

                this.clock = new THREE.Clock();
                this.animate = this.animate.bind(this);
                requestAnimationFrame(this.animate);
            }

            initEvents() {
                window.addEventListener('resize', () => {
                    this.camera.aspect = window.innerWidth / window.innerHeight;
                    this.camera.updateProjectionMatrix();
                    this.renderer.setSize(window.innerWidth, window.innerHeight);
                });
                
                window.addEventListener('mousemove', (e) => {
                    if (this.isPlaying) {
                        const cursor = document.getElementById('cursor-container');
                        cursor.style.left = e.clientX + 'px';
                        cursor.style.top = e.clientY + 'px';
                    }
                });

                window.addEventListener('mousedown', (e) => {
                    if (this.isPlaying) {
                        this.handleInput(e);
                        // Animation
                        const reticle = document.getElementById('aim-reticle');
                        reticle.classList.remove('click-pulse');
                        void reticle.offsetWidth; 
                        reticle.classList.add('click-pulse');
                    }
                });
            }

            async fetchBlockData() {
                try {
                    const res = await fetch('https://mempool.space/api/blocks/tip/height');
                    const h = await res.json();
                    this.currentBlock = h;
                    document.getElementById('menu-block').innerText = `#${h}`;
                } catch (e) {}
            }

            connectNetwork() {
                this.ws = new WebSocket("wss://ws.blockchain.info/inv");
                this.ws.onopen = () => this.ws.send(JSON.stringify({ "op": "unconfirmed_sub" }));
                this.ws.onmessage = (e) => {
                    const msg = JSON.parse(e.data);
                    if (msg.op === "utx") {
                        let val = 0; 
                        msg.x.out.forEach(o => val += o.value);
                        this.handleTransaction(val / 1e8, msg.x.hash);
                    }
                };
            }

            start() {
                this.score = 0;
                this.timeLeft = CONFIG.duration;
                this.sessionTxs = [];
                this.lootedHashes.clear();
                
                // Cleanup
                this.cubes.forEach(c => this.scene.remove(c));
                this.hitboxes.forEach(h => this.scene.remove(h));
                this.cubes = [];
                this.hitboxes = [];

                document.body.classList.add('gaming');
                UI.resetHUD();
                UI.showScreen(null); 
                this.isPlaying = true;
            }

            end() {
                this.isPlaying = false;
                document.body.classList.remove('gaming');
                const totalVal = this.sessionTxs.reduce((sum, tx) => sum + tx.val, 0);
                const missed = totalVal - this.score;
                Storage.saveScore(this.score, this.currentBlock, this.sessionTxs, this.lootedHashes);
                UI.updateGameOver(this.score, missed, this.sessionTxs, this.lootedHashes);
                UI.showScreen('screen-gameover');
            }

            handleTransaction(btc, hash) {
                UI.addFeedItem(btc);
                if (this.isPlaying) {
                    this.sessionTxs.push({ hash, val: btc });
                    this.spawnCube(btc, hash);
                }
            }

            spawnCube(btc, hash) {
                let s;
                let isSuper = false;

                if (btc > 50.0) { s = 1.0; isSuper = true; }
                else if (btc < 0.05) s = 3.5; 
                else if (btc < 0.5) s = 2.0; 
                else if (btc < 1.0) s = 1.2; 
                else s = 0.8; 

                let emissiveInt, color;
                if (isSuper) { color = CONFIG.colors.super; emissiveInt = 2.0; }
                else if (btc > 1.0) { color = CONFIG.colors.deep; emissiveInt = 1.5; } 
                else if (btc > 0.1) { color = CONFIG.colors.mid; emissiveInt = 0.5; } 
                else { color = CONFIG.colors.pale; emissiveInt = 0.1; }
                
                // 1. VISIBLE MESH
                const geo = new THREE.BoxGeometry(s, s, s);
                const mat = new THREE.MeshStandardMaterial({ 
                    color: color, roughness: 0.3, 
                    emissive: color, emissiveIntensity: emissiveInt
                });
                const mesh = new THREE.Mesh(geo, mat);

                // 2. INVISIBLE HITBOX (50% Larger)
                const hitGeo = new THREE.BoxGeometry(s * 1.5, s * 1.5, s * 1.5);
                const hitMat = new THREE.MeshBasicMaterial({ visible: false }); 
                const hitbox = new THREE.Mesh(hitGeo, hitMat);

                const r = CONFIG.spawnRange - 2; 
                const startX = (Math.random()-0.5)*r;
                const startZ = (Math.random()-0.5)*r;

                mesh.position.set(startX, CONFIG.spawnHeight, startZ);
                hitbox.position.set(startX, CONFIG.spawnHeight, startZ);
                
                const sharedData = {
                    btc: btc, hash: hash,
                    speed: 0.2 + (Math.random() * 0.4),
                    rotX: Math.random()*0.1, 
                    rotY: Math.random()*0.1,
                    isSuper: isSuper,
                    linkedMesh: mesh,
                    linkedHitbox: hitbox
                };

                mesh.userData = sharedData;
                hitbox.userData = sharedData;

                this.scene.add(mesh);
                this.scene.add(hitbox);
                
                this.cubes.push(mesh);
                this.hitboxes.push(hitbox);
            }

            handleInput(e) {
                if (!this.isPlaying) return;
                this.mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
                this.mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
                
                this.raycaster.setFromCamera(this.mouse, this.camera);
                
                // CHECK HITBOXES
                const intersects = this.raycaster.intersectObjects(this.hitboxes);

                if (intersects.length > 0) {
                    this.loot(intersects[0].object, e.clientX, e.clientY);
                }
            }

            loot(target, x, y) {
                const val = target.userData.btc;
                this.score += val;
                this.lootedHashes.add(target.userData.hash);
                
                UI.updateScore(this.score);
                UI.showPopText(val, x, y);

                const mesh = target.userData.linkedMesh;
                const hitbox = target.userData.linkedHitbox;

                this.scene.remove(mesh);
                this.scene.remove(hitbox);

                this.cubes = this.cubes.filter(c => c !== mesh);
                this.hitboxes = this.hitboxes.filter(h => h !== hitbox);
            }

            animate() {
                requestAnimationFrame(this.animate);
                const delta = this.clock.getDelta();

                if (this.isPlaying) {
                    this.timeLeft -= delta;
                    if (this.timeLeft <= 0) { this.timeLeft = 0; this.end(); }
                    UI.updateTimer(this.timeLeft);

                    for (let i = this.cubes.length - 1; i >= 0; i--) {
                        const c = this.cubes[i];
                        const h = this.hitboxes[i]; 

                        c.position.y -= c.userData.speed;
                        h.position.y -= c.userData.speed;
                        
                        const spinMult = c.userData.isSuper ? 5.0 : 1.0;
                        c.rotation.x += c.userData.rotX * spinMult;
                        c.rotation.y += c.userData.rotY * spinMult;
                        
                        h.rotation.x = c.rotation.x;
                        h.rotation.y = c.rotation.y;

                        if (c.position.y < -60) {
                            this.scene.remove(c);
                            this.scene.remove(h);
                            this.cubes.splice(i, 1);
                            this.hitboxes.splice(i, 1);
                        }
                    }
                } else {
                    const t = Date.now() * 0.0005;
                    this.camera.position.x = Math.sin(t) * 60;
                    this.camera.position.z = Math.cos(t) * 60;
                    this.camera.lookAt(0, 5, 0);
                }
                this.renderer.render(this.scene, this.camera);
            }
        }

        // --- UI MANAGER ---
        class UIManager {
            constructor() {
                this.hudTop = document.getElementById('hud-top');
                this.feedWidget = document.getElementById('feed-widget');
                this.feedList = document.getElementById('feed-list');
                this.timerEl = document.getElementById('timer-display');
                this.scoreEl = document.getElementById('score-display');
            }

            showScreen(id) {
                document.querySelectorAll('.screen-overlay').forEach(el => el.classList.remove('active'));
                if (id && id !== 'hidden') {
                    document.getElementById(id).classList.add('active');
                    this.hudTop.style.display = 'none';
                    this.feedWidget.style.display = 'none';
                    if(id === 'screen-leaderboard') this.renderLeaderboard();
                } else if (!id) {
                    this.hudTop.style.display = 'flex';
                    this.feedWidget.style.display = 'flex';
                }
            }

            resetHUD() {
                this.scoreEl.innerText = "0.00000000";
                this.timerEl.innerText = CONFIG.duration.toFixed(2);
                this.feedList.innerHTML = '';
            }

            updateScore(s) { this.scoreEl.innerText = s.toFixed(8); }
            updateTimer(t) { this.timerEl.innerText = t.toFixed(2); }

            addFeedItem(btc) {
                const row = document.createElement('div');
                row.className = 'feed-row';
                row.innerHTML = `TX <span class="feed-amt">${btc.toFixed(4)} BTC</span>`;
                this.feedList.prepend(row);
                if (this.feedList.children.length > 8) this.feedList.removeChild(this.feedList.lastChild);
            }

            showPopText(val, x, y) {
                const el = document.createElement('div');
                el.className = 'pop-float';
                el.innerText = `+${val.toFixed(4)}`;
                el.style.left = `${x}px`; el.style.top = `${y}px`;
                document.body.appendChild(el);
                setTimeout(() => el.remove(), 600);
            }

            updateGameOver(score, missed, allTxs, lootedSet) {
                document.getElementById('end-score').innerText = score.toFixed(6) + " BTC";
                document.getElementById('end-missed').innerText = missed.toFixed(6) + " BTC";
                const container = document.getElementById('log-list');
                container.innerHTML = '';
                const sorted = [...allTxs].sort((a,b) => b.val - a.val);
                sorted.forEach(tx => {
                    const isLooted = lootedSet.has(tx.hash);
                    const row = document.createElement('div');
                    row.className = 'data-row';
                    row.style.opacity = isLooted ? '1' : '0.4';
                    row.innerHTML = `
                        <div class="col-hash">${tx.hash}</div>
                        <div class="col-val">${tx.val.toFixed(6)}</div>
                        <div style="font-size:10px; font-weight:bold; color:${isLooted?'var(--highlight)':'#555'}; min-width:60px; text-align:right">
                            ${isLooted ? 'MINED' : 'MISSED'}
                        </div>
                    `;
                    container.appendChild(row);
                });
            }

            renderLeaderboard() {
                const container = document.getElementById('leaderboard-list');
                container.innerHTML = '';
                const data = Storage.getScores();
                if(data.length === 0) { container.innerHTML = '<div style="padding:20px; text-align:center;">No scores yet.</div>'; return; }
                data.forEach((entry, i) => {
                    const row = document.createElement('div');
                    row.className = 'data-row';
                    row.style.cursor = 'pointer';
                    row.innerHTML = `
                        <div style="display:flex; gap:15px; color:#fff">
                            <span style="color:#555; width:25px">#${i+1}</span>
                            <span>Block #${entry.block}</span>
                        </div>
                        <div class="col-val">${entry.score.toFixed(6)} BTC</div>
                    `;
                    row.onclick = () => this.openModal(entry);
                    container.appendChild(row);
                });
            }

            openModal(entry) {
                const container = document.getElementById('modal-list');
                container.innerHTML = '';
                const lootedSet = new Set(entry.lootedTxs);
                const lootedList = entry.allTxs.filter(tx => lootedSet.has(tx.hash)).sort((a,b) => b.val - a.val);
                if(lootedList.length === 0) container.innerHTML = '<div style="padding:20px;">No data.</div>';
                lootedList.forEach(tx => {
                    const row = document.createElement('div');
                    row.className = 'data-row';
                    row.innerHTML = `<div class="col-hash">${tx.hash}</div><div class="col-val">${tx.val.toFixed(6)}</div>`;
                    container.appendChild(row);
                });
                document.getElementById('screen-modal').classList.add('active');
            }
        }

        // --- STORAGE ---
        const Storage = {
            KEY: 'btc_miner_v21_scores',
            saveScore(s, block, allTxs, lootedSet) {
                if(s === 0) return;
                const data = this.getScores();
                data.push({ score: s, block: block, date: Date.now(), allTxs: allTxs, lootedTxs: Array.from(lootedSet) });
                data.sort((a, b) => b.score - a.score);
                localStorage.setItem(this.KEY, JSON.stringify(data.slice(0, 50)));
            },
            getScores() { return JSON.parse(localStorage.getItem(this.KEY) || '[]'); }
        };

        const UI = new UIManager();
        const Game = new GameManager();

    </script>
</body>
</html>
"""

# --- BUILDER LOGIC ---
print(f"✅ Generated: {OUTPUT_FILE}")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)