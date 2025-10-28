/* 
Welcome to Rattack! I coded this over a period of a month or so and there is a lot I would still improve 
but I'm fairly happy with the functional result. The code uses the three.js library to create a rendered
3D game. The most important functions have comments explaining their purpose.
*/


import * as THREE from 'three';
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { MapControls } from 'three/addons/controls/MapControls.js';
import { degToRad, radToDeg } from 'three/src/math/MathUtils.js';
import { AnimationMixer } from 'three';
import { DragControls } from 'three/examples/jsm/controls/DragControls.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

// instantiate the scene

const scene = new THREE.Scene();

// instantiate the Loader

const loader = new GLTFLoader();

// add ambient light and a side light to the scene

const unitLightcolor = 0xFFFFFF;
const unitLightIntensity = 9;
const unitLight = new THREE.DirectionalLight(unitLightcolor, unitLightIntensity);
unitLight.position.set(110, 90, -15);
unitLight.target.position.set(0, 0, -20);
unitLight.castShadow = false;

scene.add(unitLight);
scene.add(unitLight.target);

const light = new THREE.AmbientLight(0x404040, 0);
scene.add( light );

// instantiaite the camera

const canvas = document.querySelector('canvas.threejs')

const camera = new THREE.PerspectiveCamera(30, (window.innerWidth) / (window.innerHeight), 0.1, 150)
camera.position.set(30, 80, 20);

scene.add(camera)

// instantiate camera controls

const controls = new MapControls( camera, canvas );
controls.enableDamping = true;
controls.target.set(30, 0, -15);   
controls.saveState();
controls.update(); 

// instantiate the renderer with alpha for transparency

const renderer = new THREE.WebGLRenderer(
  {canvas: canvas,
  alpha: true}
);

// set scene background colour and size of renderer to the window's width and height

renderer.setClearColor(0xffffff, 0);
renderer.setSize(window.innerWidth, window.innerHeight);

// add sound to the camera and load sounds

const audioLoader = new THREE.AudioLoader(); 
const listener = new THREE.AudioListener();
camera.add( listener );

const soundBuffers = {
tankFireBuffer: "tankFire",
chaffFireBuffer: "chaffFire",
batFireBuffer: "batFire",
tronFireBuffer: "tronFire",
gameMusicBuffer: "gameMusic"
}

// gamemusic must be declared here as it is not contained within a unit method

let gameMusic = null;

function autoLoadSounds (soundBuffers) {
  for (let key of Object.keys(soundBuffers)) {
  const sound = soundBuffers[key];
  audioLoader.load(`Assets/sounds/${sound}.mp3`, function(buffer) {
    soundBuffers[key] = buffer;
    if (key === "gameMusicBuffer") {
      gameMusic = new THREE.Audio(listener);
      gameMusic.setBuffer(buffer);
      gameMusic.setLoop(true);
      let gameMusicVolume = 0.3;
      gameMusic.setVolume(gameMusicVolume);
    }
  });
}
}

autoLoadSounds(soundBuffers);

// add sprite materials for firing of weapons, these have the name of tankAttackMaterial but apply for all units

const tankAttackMap1 = new THREE.TextureLoader().load( 'Assets/Textures/sprites/tank-attack/tankattack01.png', () => {
  console.log('Texture loaded!')
} );
const tankAttackMaterial1 = new THREE.SpriteMaterial( { map: tankAttackMap1, transparent: true } );

const tankAttackMap2 = new THREE.TextureLoader().load( 'Assets/Textures/sprites/tank-attack/tankattack02.png', () => {
  console.log('Texture loaded!')
}  );
const tankAttackMaterial2 = new THREE.SpriteMaterial( { map: tankAttackMap2, transparent: true } );

const attackSpriteTest = new THREE.Sprite( tankAttackMaterial2 );
attackSpriteTest.position.set(0,1,0);
scene.add(attackSpriteTest);

/* particle system which is called by unit objects and creates travelling particles that represent unit projectiles
 the particle size and speed can be controlled for each unit by changing values in the swtich statement in the weaponParticle function*/

function weaponParticle(unitTargetDirection, unitTargetPosition, attackPoint, unitName) {
  
  if (unitName != "ratoTron") {

  let particleSize;
  let particleColour;
  let particleSpeed;

  switch (unitName) {
    case "ratTank": 
    particleSize = 0.5;
    particleColour = new THREE.Color().setHex( 0x1c0504 );
    particleSpeed = 0.2
    break;
    case "ratChaff": particleSize = 0.3
    particleColour = new THREE.Color().setHex( 0xfdff6e ); 
    particleSpeed = 0.3;
    break;
    case "ratBat": particleSize = 0.25
    particleColour = new THREE.Color().setHex( 0xfdff6e );
    particleSpeed = 0.4;
  }
  
  const sphereGeometry = new THREE.SphereGeometry(0.1,2,2)
  const sphereMaterial = new THREE.PointsMaterial({
  size: particleSize,
  color: particleColour
})

// each particle is made from a sphere geometry with a point material and "ticks" forward by the calculated amount once per frame

const sphere = new THREE.Points(sphereGeometry, sphereMaterial);
sphere.position.copy(attackPoint);
scene.add(sphere);

const tick = () => {
    const particleDirection = new THREE.Vector3().copy(unitTargetDirection).normalize();
    sphere.position.addScaledVector(particleDirection, particleSpeed);

    
  if (sphere.position.distanceTo(attackPoint) < unitTargetPosition.distanceTo(attackPoint)) {
    window.requestAnimationFrame(tick);
  } else {
    scene.remove(sphere);
  }
}

tick();
  }
}

// define variables that store the player funds, and what units can be bought from the shop as well as an array to store shop button objects

let currentFunds = 0;
const currentShopStock = [
  {
  name: "ratChaff", 
  cost: 50, 
  airVsGround: "ground", 
  canAttack: "air & ground" 
  }, 
  {name :"ratTank", 
  cost: 150,
  airVsGround: "ground",
  canAttack: "air & ground"
  }, 
  {name: "ratBat",
  cost: 125,
  airVsGround: "ground",
  canAttack: "air & ground"
  },
  {name: "ratoTron",
  cost: 500,
  airVsGround: "ground",
  canAttack: "ground"
  }
  ];

const unitShop = []
const shopButtons = []

let selectedShopButton = null;
let lastHighlightedGridCell = null;

// add funds display to the top right of the screen displaying player's available funds

const fundsDisplay = document.createElement('div');
fundsDisplay.id = 'funds-counter';
fundsDisplay.style.position = 'fixed';
fundsDisplay.style.top = '20px';
fundsDisplay.style.right = '30px';
fundsDisplay.style.background = 'rgba(255, 220, 120, 0.95)';
fundsDisplay.style.color = '#222';
fundsDisplay.style.fontSize = '2rem';
fundsDisplay.style.fontFamily = 'monospace';
fundsDisplay.style.padding = '12px 32px';
fundsDisplay.style.borderRadius = '12px';
fundsDisplay.style.zIndex = '2002';
fundsDisplay.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
fundsDisplay.textContent = `Funds: ${currentFunds}`;
document.body.appendChild(fundsDisplay);

// add a clock element at the top of the screen. This clock counts down during the battle phase

const battleTimerDisplay = document.createElement('div');
battleTimerDisplay.id = 'battle-timer';
battleTimerDisplay.style.position = 'fixed';
battleTimerDisplay.style.top = '20px';
battleTimerDisplay.style.left = '50%';
battleTimerDisplay.style.transform = 'translateX(-50%)';
battleTimerDisplay.style.background = 'rgba(80, 120, 255, 0.95)';
battleTimerDisplay.style.color = 'white';
battleTimerDisplay.style.fontSize = '2rem';
battleTimerDisplay.style.fontFamily = 'monospace';
battleTimerDisplay.style.padding = '12px 32px';
battleTimerDisplay.style.borderRadius = '12px';
battleTimerDisplay.style.zIndex = '2002';
battleTimerDisplay.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
battleTimerDisplay.textContent = '';
battleTimerDisplay.style.display = 'none'; // Hidden by default
document.body.appendChild(battleTimerDisplay);

window.addEventListener('resize', () =>{
  
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
})

// add drag controls to the scene which can be swapped out with map Controls between the rounds

const dragControls = new DragControls(unitShop, camera, renderer.domElement);
dragControls.transformGroup = true;

// declare floating cursor which is used to create the small icons that follow the cursor when player is placing units

const floatingCursor = document.createElement('img');
floatingCursor.style.position = 'fixed';
floatingCursor.style.pointerEvents = 'none';
floatingCursor.style.width = '48px';
floatingCursor.style.height = '48px';
floatingCursor.style.zIndex = '9999';
floatingCursor.style.display = 'none'; // Hidden by default
document.body.appendChild(floatingCursor);

document.addEventListener('mousemove', (e) => {
  if (floatingCursor.style.display === 'block') {
    floatingCursor.style.left = `${e.clientX + 8}px`;
    floatingCursor.style.top = `${e.clientY + 8}px`;
  }
});

// load in the floor, which is effectively the toyshop background scene, as well as an array for storing the mesh grid objects for raycasting 

let floor = null;
const displayedGridMeshes = [];

loader.load( `/Assets/placeholder_models/floor.glb`, function ( gltf ) {
  floor = gltf.scene;
  floor.position.set(0,-0.1,0);
  floor.scale.set(1,1,1);
  scene.add(floor);

}, undefined, function ( error ) {

  console.error( error );

} );
 

// variables for the FPS display, which should be kept in the game for debugging purposes

let lastTime = performance.now();
let frames = 0;
let fps = 0;

// FPS display elements that appear on screen
const fpsDisplay = document.createElement('div');
fpsDisplay.style.position = 'fixed';
fpsDisplay.style.top = '10px';
fpsDisplay.style.left = '10px';
fpsDisplay.style.background = 'rgba(0,0,0,0.7)';
fpsDisplay.style.color = 'white';
fpsDisplay.style.fontFamily = 'monospace';
fpsDisplay.style.padding = '4px 8px';
fpsDisplay.style.zIndex = 1000;
fpsDisplay.textContent = 'FPS: 0';
document.body.appendChild(fpsDisplay);

// pointer function for identifying objects

const pointer = new THREE.Vector2();
function onPointerMove( event ) {

	// calculate pointer position in normalized device coordinates
  const rect = renderer.domElement.getBoundingClientRect();
  pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  pointer.y = - ((event.clientY - rect.top) / rect.height) * 2 + 1;

}

window.addEventListener( 'pointermove', onPointerMove );

// set variable that the unit placement raycaster is not active

let placementRaycasterActive = false;

// set the game clock

const clock = new THREE.Clock();

/* set variables for player turns and higher-order game logic such as what "phase" the game is in. In
the placement phase units can be placed, but they don't move or attack. In the battle phase
most ui elements disappear and the player must wait for units' battle to resolve. These variables
store things like the duration of a battle phase, the funds in the opponent and player bank etc
*/
let battleWinCheckInterval = null;
let startBattleButtonContainer = null;
let currentGameRound = 0;
const gamePhases = ["placement", "battle"]
let currentPhaseIndex = 0
let battlePhaseDuration = 30; 
let battlePhaseRemaining = battlePhaseDuration;
let opponentFunds;
let enemyUnitsPreview = [];
let attacksAndMovementEnabler = false;
let roundResolved = false;

// declare player and opponent health. These variables are adjusted as the game progresses and each round resolves.

let playerHealth = 50;
let opponentHealth = 50;

// Player health display (top left)
const playerHealthDisplay = document.createElement('div');
playerHealthDisplay.id = 'player-health';
playerHealthDisplay.style.position = 'fixed';
playerHealthDisplay.style.top = '20px';
playerHealthDisplay.style.left = '30px';
playerHealthDisplay.style.background = 'rgba(120, 255, 120, 0.95)';
playerHealthDisplay.style.color = '#222';
playerHealthDisplay.style.fontSize = '2rem';
playerHealthDisplay.style.fontFamily = 'monospace';
playerHealthDisplay.style.padding = '12px 32px';
playerHealthDisplay.style.borderRadius = '12px';
playerHealthDisplay.style.zIndex = '2002';
playerHealthDisplay.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
playerHealthDisplay.textContent = `Player Health: ${playerHealth}`;
document.body.appendChild(playerHealthDisplay);

// Opponent health display (top right)
const opponentHealthDisplay = document.createElement('div');
opponentHealthDisplay.id = 'opponent-health';
opponentHealthDisplay.style.position = 'fixed';
opponentHealthDisplay.style.top = '20px';
opponentHealthDisplay.style.right = '300px';
opponentHealthDisplay.style.background = 'rgba(255, 120, 120, 0.95)';
opponentHealthDisplay.style.color = '#222';
opponentHealthDisplay.style.fontSize = '2rem';
opponentHealthDisplay.style.fontFamily = 'monospace';
opponentHealthDisplay.style.padding = '12px 32px';
opponentHealthDisplay.style.borderRadius = '12px';
opponentHealthDisplay.style.zIndex = '2002';
opponentHealthDisplay.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
opponentHealthDisplay.textContent = `Opponent Health: ${opponentHealth}`;
document.body.appendChild(opponentHealthDisplay);

// game controller function which is called and invokes the relevant function that starts the next game phase

function gamePhaseController () {
  const phase = gamePhases[currentPhaseIndex];
 switch (phase) {
    case "placement":
      currentFunds += (currentGameRound * 50 + 100)
      updateFundsDisplay();
      startPlacementPhase();
      break;
    case "battle":
      startBattlePhase();
      break;
  }


}

// placement phase function which invokes all other functions necessary for the placement phase to occur

function startPlacementPhase () {
  
  
  // reset the camera and lock the map controls so player is in a fixed view
  camera.position.set(30, 80, 20);
  controls.reset();
  controls.enabled = false;
  dragControls.enabled = true;
  gameMusic.setVolume(0.3);
  
  // update the health displays of the player and opponent

  updateHealthDisplays();

  // add invreasing funds to the opponents' wallet with every round

  opponentFunds = currentGameRound * 50 + 100

  // remove all units from the previous round that are still on the board. This refers to their meshes and materials

  boardUnitCleanUp();
  
  // instantiate the shop buttons

  addShopButtons();

  // fire up the raycaster so the player can highlight the grid squares and place units

  placementRaycaster();

  // calculate where enemy units can be placed this round

  enemyPlacementController();

  // the unit initialiser adds all previously placed units back on the board, but doesn't yet add the new enemy units
  // this round so that they are hiddun until the start battle button is pressed. hidden enemy units stored in separate array.

  unitInitialiser(placementBoard);

  // add unit previews to the top of the screen based on what enemy units are deploying this round

  unitPreviewInitialiser();


  // add a grid of meshes for raycasting on board points (and thereby placing units). Default visibility is false,
  // and when players cursor over them, they are visible again. Not "transparent" because this is too resource intensive.

  for (let i = 0; i < 40; i++) {
    if (i >= 19) {
      continue;
    }
  for (let j = 0; j < 60; j++) {
  const geometry = new THREE.PlaneGeometry( 1, 1); 
  const material = new THREE.MeshBasicMaterial( {color: 0x88E788} ); 
  const plane = new THREE.Mesh( geometry, material ); 
  plane.position.set(j, 0, (i * -1));
  plane.rotation.set(degToRad(-90),0,0)
  displayedGridMeshes.push(plane);
  
  plane.visible = false;
  scene.add( plane );
  }
}


// The start battle button added so the player can enter the battle phase whenever they choose

addStartBattleButton();

}

/* The battle phase function. It invokes all the relevant functions that control battle phase such as initialising
hidden enemy units, and enables the movement and attack controller so that units start fighting.
There is a timeout set for the latter parts of the function due to the async loading of units creating errors, so
it was easiest just to get the function to wait a short while before proceeding.
*/

function startBattlePhase() {
  
  // add enemy units that are deploying this round but were hidden during placement phase
  unitInitialiser(hiddenUnitsPlacementBoard);

  // clear this array so that the units are not duplicated / added every subsequent round
  clearHiddenUnitsPlacementBoard();

  // get rid of the unit preview at top of screen and clear its array
  removeEnemyUnitsPreview();
  enemyUnitsPreview.length = 0;

  gameMusic.setVolume(0.12);
  roundResolved = false;

  setTimeout(() => {
 
    // controls switched back to more free map controls so that player can zoom and pan a bit

 controls.reset();
  controls.enabled = true;
  dragControls.enabled = false;

  // remove the shop buttons!
  shopButtons.forEach((button) => {
    button.remove();
  }
  );
  startBattleButtonContainer.remove();
  startBattleButtonContainer = null;
  shopButtons.length = 0;

  // VERY IMPORTANT - if this is not enabled, the function controlling movement and attack won't run and the phase won't start

  attacksAndMovementEnabler = true;

  // make sure the placement grid planes for raycasting aren't visible

  for (const plane of displayedGridMeshes) {
    plane.visible = false;
  }

  // ensure timings are set up properly and start teh clock!

   battlePhaseRemaining = battlePhaseDuration;
    battleTimerDisplay.style.display = 'block';
    clock.start();

    // This function checks once per second to see if all units on either side are dead, or if the timer has run out
    // in each instance it invokes a round resolve alert, and amends player / opponent health appropriately
    // if player or opponent health drops below zero it's game over!

    if (battleWinCheckInterval) clearInterval(battleWinCheckInterval);
    
    battleWinCheckInterval = setInterval(() => {
    const allPlayerUnitsDead = !activeUnits.some(unit => unit.playerAlignment === "player" && unit.status === "alive");
    const allOpponentUnitsDead = !activeUnits.some(unit => unit.playerAlignment === "opponent" && unit.status === "alive");
    if (allPlayerUnitsDead) {

      console.log("allPlayerUnitsDead!");
      const remainingOpponentUnits = activeUnits.filter((unit) => unit.status === "alive" && unit.playerAlignment === "opponent").length
      playerHealth -= remainingOpponentUnits;
      updateHealthDisplays();
      roundResolveAlert("Opponent", "Player", remainingOpponentUnits);
      clock.stop();
      attacksAndMovementEnabler = false;
      stopAllAttacks();
      clearInterval(battleWinCheckInterval);

    } else if (allOpponentUnitsDead) {

      console.log("allOpponentUnitsDead!");
      const remainingPlayerUnits = activeUnits.filter((unit) => unit.status === "alive" && unit.playerAlignment === "player").length
      opponentHealth -= remainingPlayerUnits; 
      updateHealthDisplays();
      roundResolveAlert("Player", "Opponent", remainingPlayerUnits);
       clock.stop();
       attacksAndMovementEnabler = false;
       stopAllAttacks();
      clearInterval(battleWinCheckInterval);

       } else if (!allOpponentUnitsDead && !allPlayerUnitsDead && battlePhaseRemaining <=0) {

        console.log("Draw!");
        const draw = true;
        const remainingPlayerUnits = activeUnits.filter((unit) => unit.status === "alive" && unit.playerAlignment === "player").length
        const remainingOpponentUnits = activeUnits.filter((unit) => unit.status === "alive" && unit.playerAlignment === "opponent").length
        opponentHealth -= remainingPlayerUnits;
        playerHealth -= remainingOpponentUnits;
        updateHealthDisplays();
        roundResolveAlert("Player", "Opponent", remainingOpponentUnits, draw, remainingPlayerUnits);
        clock.stop();
        attacksAndMovementEnabler = false;
        stopAllAttacks();
        clearInterval(battleWinCheckInterval);
      }

  }, 1000); 
  }, 500);
}


// The animation loop which performs a bunch of vital functions every frame like updating renderer, camera, and raycasting

function animate() {
  
  // Highlight planes on hover during placement phase
if (currentPhaseIndex === 0 && selectedShopButton) {
  // Reset all planes to default color

  // Raycast from pointer
  raycaster.setFromCamera(pointer, camera);
  const intersects = raycaster.intersectObjects(displayedGridMeshes);

    if (intersects.length > 0) {
    const hoveredCell= intersects[0];
    if (lastHighlightedGridCell && lastHighlightedGridCell !== hoveredCell) {
      lastHighlightedGridCell.object.visible = false;
    }
    hoveredCell.object.visible = true;
    lastHighlightedGridCell = hoveredCell;
  } else if (lastHighlightedGridCell) {
    lastHighlightedGridCell.object.visible = false;
    lastHighlightedGridCell = null;
  }
}

frames++;
  const now = performance.now();
  if (now - lastTime >= 1000) {
    fps = frames;
    frames = 0;
    lastTime = now;
    fpsDisplay.textContent = `FPS: ${fps}`;
  }

// get the delta from the game clock (so this is running to a set speed not animation refresh rate)
  const delta = clock.getDelta();


  
  if (clock.elapsedTime > 30 && currentPhaseIndex === 1) {
    
    clock.stop();
    
  }

  for (let unit of activeUnits) {
  if (unit.mixer) {
    unit.mixer.update(delta);
  }
}

if (currentPhaseIndex === 1) {
  if (attacksAndMovementEnabler) {
  movementAttackController();
  }
  battlePhaseRemaining = (battlePhaseDuration - clock.getElapsedTime());
  if (battlePhaseRemaining < 0) {
    battlePhaseRemaining = 0;}
  battleTimerDisplay.textContent = `Battle Time: ${battlePhaseRemaining.toFixed(1)}s`;
  if (battlePhaseRemaining === 0) {
    battleTimerDisplay.style.display = 'none';
}

} else {
  battleTimerDisplay.style.display = 'none';
}

  renderer.render(scene, camera);
  controls.update();

}

renderer.setAnimationLoop( animate );


// create an array that stores all unit objects currently active in the round

let activeUnits = [];

// The unitInfo object allows easy customisation of unit properties and then gets fed into the unitfactory function which
// creates unit objects

const unitInfo = {
  ratChaff: {
    health: 40, damage: 10, damage_interval: 1, armour: 0, range: 4, speed: 0.012, turningSpeed: 1,
    fieldOfView: 45, _size: 0.5, airborne: "no", canAttack: "both", shadowScale: 0.8,
    attackSoundBuffer: "chaffFireBuffer", spriteScale: 0.7, minVolume: 0.1, maxVolume: 0.9, damageTimeOut: 800
  },
  ratTank: {
    health: 150, damage: 30, damage_interval: 2, armour: 2, range: 8, speed: 0.01, turningSpeed: 0.25,
    fieldOfView: 5, _size: 1.0, airborne: "no", canAttack: "ground", shadowScale: 2.7,
    attackSoundBuffer: "tankFireBuffer", spriteScale: 1, minVolume: 0.2, maxVolume: 0.8, damageTimeOut: 1800
  },
  ratBat: {
    health: 30, damage: 15, damage_interval: 1.2, armour: 0, range: 6, speed: 0.03, turningSpeed: 2,
    fieldOfView: 45, _size: 0.5, airborne: "yes", canAttack: "both", shadowScale: 0.8,
    attackSoundBuffer: "batFireBuffer", spriteScale: 0.5, minVolume: 0.1, maxVolume: 0.33, damageTimeOut: 1000
  },
  ratoTron: {
    health: 500, damage: 150, damage_interval: 2, armour: 0, range: 4, speed: 0.015, turningSpeed: 1, 
    fieldOfView: 25, _size: 4, airborne: "no", canAttack: "ground", shadowScale: 3,
    attackSoundBuffer: "tronFireBuffer", spriteScale: 0.7, minVolume: 0.1, maxVolume: 0.7, damageTimeOut: 1800
  }
};

/* The unit factore function creates objects that contain all important unit properties, the unit mesh object as imported
by the GLFG loader (.mesh) and the various methods like attacking, dying, and animating. Some properties from three.js
objects are referenced by top-level properties for ease of access. 
*/

const unitFactory = function (unitName, playerAlignment, x, z) {
 const importedUnitInfo = unitInfo[unitName];
 console.log(importedUnitInfo);

  return {
  _name: `${unitName}`,
    get name() {
  return this._name;
  },
  playerAlignment: playerAlignment,
  health: importedUnitInfo.health,
  damage: importedUnitInfo.damage,
  damage_interval: importedUnitInfo.damage_interval,
  armour: importedUnitInfo.armour,
  range: importedUnitInfo.range,
  speed: importedUnitInfo.speed,
  turningSpeed: importedUnitInfo.turningSpeed,
  fieldOfView: importedUnitInfo.fieldOfView,
  _size: importedUnitInfo._size,
  get size() {return this._size;},
  airborne: importedUnitInfo.airborne,
  canAttack: importedUnitInfo.canAttack,
  _status: "alive",
 set status(val) {
    this._status = val;
  },
  get status() {return this._status;},
  _target: null,
   set target(val) {
    this._target = val;
  },
  get target() {
  return this._target;
  },
   _lastTarget: null,
   set lastTarget(val) {
    this._lastTarget = val;
  },
  get lastTarget() {
  return this._lastTarget;
  },
  targetDirection: null,
  positionStart: new THREE.Vector3(x, 0, z),
  position: new THREE.Vector3(x, 0, z),
  mesh: null,
  shadow: null,
  shadowScale: importedUnitInfo.shadowScale,
  meshMaterials: [],
  meshOpacities: [],
  nearestEnemy: [0, 0],
  attackSoundBuffer: importedUnitInfo.attackSoundBuffer,
  animationActionStash: {
    attack: null,
    movement: null,
    death: null
    
  },
  attackPoint: null,
  cooldownUntil: 0,
  playAnimation (animation) {
      this.animationActionStash.attack.reset();

      if (animation === 'death') {
        this.animationActionStash.attack.stop();
        this.animationActionStash.movement.stop();
      this.animationActionStash.death.setLoop(THREE.LoopOnce, 1); 
      this.animationActionStash.death.clampWhenFinished = true;
      this.animationActionStash.death.play();
    } else if (animation === 'attack') {
        
      if (this.animationActionStash.movement.isRunning()) {
        this.animationActionStash.movement.stop();
        this.animationActionStash.movement.reset();
    }
      this.animationActionStash.attack.setLoop(THREE.LoopOnce, 1); 
      this.animationActionStash.attack.clampWhenFinished = true;
      this.animationActionStash.attack.play();      
    } else if (animation === 'movement' && !this.animationActionStash.movement.isRunning() && !this.animationActionStash.attack.isRunning()) {
      this.animationActionStash.movement.setLoop(THREE.LoopRepeat, Infinity); 
      this.animationActionStash.movement.play();   
    } if (animation === 'movement' && this.animationActionStash.movement.isRunning()) {
      
    }
},
  attackAction () {
    console.log(`the time is ${performance.now()} the cooldown is ${this.cooldownUntil}`);
  if (this.target && this.target.health > 0) {
    
    this.target.health = this.target.health-(this.damage-this.target.armour);
    
    if (!this.animationActionStash.attack.isRunning()) {
    this.playAnimation('attack');
    }

    if (this.name != "ratoTron") {
    const worldPos = new THREE.Vector3();
    this.mesh.attackPoint.getWorldPosition(worldPos);

    this.attackSprite();
     weaponParticle(this.targetDirection, this.target.position, worldPos, this.name);
    }

    this.attackSound();

    if (this.target.health <= 0) {
      this.target.death();
      

      if (this._attackInterval) {
      setTimeout(() => {
        console.log(`clearing attack interval via attackAction! ${this.name}`);
        this.target = null;
        clearInterval(this._attackInterval); 
      }, importedUnitInfo.damageTimeOut);  
       
      } 
    } 
  }
},
death () {
  this.status = "dead";
  if (this._attackInterval) {
    console.log(`clearing attack interval via death! ${this.name}`);
    clearInterval(this._attackInterval);
    this._attackInterval = null;
  }
  this.playAnimation('death');

   for (const otherUnit of activeUnits) {
    if (otherUnit.target === this) {
      otherUnit.cooldownUntil = performance.now() + otherUnit.damage_interval * 1000;
      if (otherUnit._attackInterval) {
        clearInterval(otherUnit._attackInterval);
        otherUnit._attackInterval = null;
      }
    }
  }

  this._fadeInterval = setInterval(() => {
    let fadeComplete = false;
    for (const material of this.meshMaterials) {
      material.transparent = true;
    }
    for (const material of this.meshMaterials) {
      if (material.opacity >= 0.05) {
        material.opacity = material.opacity - 0.02;
      } else if (material.opacity  < 0.05) {
      fadeComplete = true;
      }
      if (fadeComplete) {
        
        materialCleanUp();
      clearInterval(this._fadeInterval);
      }
    } 
  }, 75);
  
  const materialCleanUp = () => {
  this.mesh.traverse(obj => {
    if (obj.isMesh) {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) {
        if (Array.isArray(obj.material)) {
          obj.material.forEach(mat => mat.dispose());
        } else {
          obj.material.dispose();
        }
      }
    }
  });
  scene.remove(this.mesh);
}
}, 
attack () {
  console.log(`Attack called on ${this.name}`)
  if (this.status === "dead" || this._attackInterval) return;  
  if (performance.now() < this.cooldownUntil) return;
  console.log(performance.now());
  this.attackAction();
  this._attackInterval = setInterval(() => this.attackAction(), this.damage_interval * 1000);
},
attackSprite () {
      const attackSprite = new THREE.Sprite( tankAttackMaterial1 );
      const worldPos = new THREE.Vector3();
      this.mesh.attackPoint.getWorldPosition(worldPos);
      attackSprite.position.copy(worldPos);
      
      attackSprite.material.depthTest = false;
      attackSprite.material.depthWrite = false;
      
      
      attackSprite.scale.set(importedUnitInfo.spriteScale, importedUnitInfo.spriteScale, importedUnitInfo.spriteScale);
       scene.add( attackSprite );  
       setTimeout(() => {
    attackSprite.material = tankAttackMaterial2
    
    attackSprite.material.depthTest = false;
    attackSprite.material.depthWrite = false;
      }, 200);  
      setTimeout(() => {
    scene.remove(attackSprite);
      }, 500);  
},
attackSound () {
    
  if (soundBuffers[this.attackSoundBuffer]) {
    
    const sound = new THREE.Audio(listener);
    sound.setBuffer(soundBuffers[this.attackSoundBuffer]);
    sound.setLoop(false);

    // Calculate distance from unit to camera's target (board center)
    const cameraTarget = controls.target;
    const unitPos = this.mesh.position;
    const distance = unitPos.distanceTo(cameraTarget);

    // Set volume based on distance (closer to center = louder)
    const maxDistance = 10;
    const minVolume = importedUnitInfo.minVolume;
    const maxVolume = importedUnitInfo.maxVolume;
    let volume = maxVolume - (distance / maxDistance) * (maxVolume - minVolume);
    volume = Math.max(minVolume, Math.min(maxVolume, volume));

    sound.setVolume(volume);
    sound.play();

    setTimeout(() => {
      sound.stop();
      if (sound.parent) sound.parent.remove(sound);
    }, 1500);
  }
}
}

}


// instantiate a 2D matrix which forms the basis for the placement board where allied and enemy unit placements are stored. The hidden board
// is there to store enemy units in the round they are deployed but before they should be displayed.

const boardWidth = 60;
const boardDepth = 40;

let placementBoard =  [];
let hiddenUnitsPlacementBoard = [];

function boardCreator(board) {

for (let i = 0; i < boardDepth; i++) {
    board.push([]);
  for (let j = 0; j < boardWidth; j++)  {
    board[i].push("empty");
  }
}
}

boardCreator(placementBoard);
boardCreator(hiddenUnitsPlacementBoard);

let playerUnitCount = 0;
let EnemyUnitCount = 0;



// function that goes through each row of the placement array and invokes addUnit to place relevant units there




// function that adds units to the array storing units for this round by importing their gltf files. While adding, it also
// traverses unit objects to replace their materials with toon shaders and places those materials in array in the unit object
// as well as creating a shadow plane and attaching it to the mesh, putting the object animations in an array, and ensuring
// that unit objects are orientated in the right direction by rotating child empties so that allied units aren't backwards

const addUnit = function(unit, playerAlignment, x, z) {

  loader.load( `/Assets/placeholder_models/${unit}.glb`, function ( gltf ) {
    activeUnits.push(unitFactory(unit, playerAlignment, x, z));
    const newUnit = activeUnits[activeUnits.length - 1];
      newUnit.mesh = gltf.scene;
      newUnit.mesh.position.copy(newUnit.position);

      newUnit.mesh.traverse(child => {
      if (child.isMesh) {
    
      const toonMaterial = new THREE.MeshToonMaterial({
      name: child.material.name,
      color: child.material.color,
      map: child.material.map,
      normalMap: child.material.normalMap,
      transparent: true,
      opacity: child.material.opacity
      });
     child.material = toonMaterial;
      } 
      
      });



      const shadow = createShadow(newUnit);
      newUnit.mesh.add(shadow);
      newUnit.shadow = shadow;
    
      function collectMaterialColoursAndOpacity(object) {
        object.traverse(child => {
        if (child.isMesh && child.material && !newUnit.meshMaterials.includes(child.material)) {
            
            newUnit.meshMaterials.push(child.material);
        } 
        }
        );
        }

        newUnit.meshMaterials = [];
       collectMaterialColoursAndOpacity(newUnit.mesh);

      
        for (let material of newUnit.meshMaterials) {
          if (material.name === "Main" && playerAlignment === "player") {
            material.color = new THREE.Color().setHex( 0x4267E7 );
          }
        }
      
      

      function storeAttackPoint(object) {
        object.traverse(child => {
          if (child.name && child.name === "attackPoint") {
            newUnit.mesh.attackPoint = child;
          }
        }

        )
      }

      storeAttackPoint(newUnit.mesh);
    

      if (gltf.animations && gltf.animations.length > 0) {
    newUnit.mixer = new THREE.AnimationMixer(gltf.scene);
    newUnit.animations = gltf.animations;
    const addAnimations = ['movement', 'attack', 'death'];
         for (const animationClipName of addAnimations) {
        const newAnimationClip = THREE.AnimationClip.findByName(newUnit.animations, `${animationClipName}`);
        const newAction = newUnit.mixer.clipAction(newAnimationClip);
        newUnit.animationActionStash[animationClipName] = newAction;
         }
        }

      if (newUnit.mesh.position.z > -20) {
        switch (unit) {
        case "ratChaff":
          newUnit.mesh.children[0].rotation.set(0,0,0);
          //newUnit.mesh.children[0].material.color.setHex(0xE767C7);
          
          break;
        case "ratBat":
          newUnit.mesh.children[0].rotation.set(0,0,0);
          
          break;
        case "ratTank":
          newUnit.mesh.children[0].rotation.set(0,0,0);
          break;
        case "ratoTron":
          newUnit.mesh.children[0].rotation.set(0,3.14159265,0)
        }
      }
      
      scene.add(newUnit.mesh);

}, undefined, function ( error ) {

  console.error( error );

} );
}


// adds an intro card on loading

const introImg = document.createElement('img');
introImg.src = 'Assets/Textures/Intro card/intro-card-01.png'; // Replace with your actual image path
introImg.style.position = 'fixed';
introImg.style.left = '50%';
introImg.style.top = '50%';
introImg.style.width = '1080px';
introImg.style.height = '1080px';
introImg.style.transform = 'translate(-50%, -50%)';
introImg.style.zIndex = '2000'; 

document.body.appendChild(introImg);

const introBtn = buttonMaker(
  '300px', 
  '80px', 
  'Start Game',
  () => {
    introImg.remove();
    introBtn.remove();
    currentGameRound++;
    gamePhaseController();
    gameMusic.play();
  }
);
introBtn.style.position = 'fixed';
introBtn.style.left = '50%';
introBtn.style.top = 'calc(50% + 570px)';
introBtn.style.transform = 'translateX(-50%)';
introBtn.style.zIndex = '2001';

document.body.appendChild(introBtn);

/* The FNEAA function iterates over every unit in the activeUnits array and finds their nearest enemy and allied units allowing
units to always have a target set (enemies) and avoid stacking on allies.
*/

function findNearestEnemyAndAlly(unit, unitsArray) {
  let nearestEnemy = null;
  let nearestAlly = null;
  let minimumDistanceEnemy = Infinity;
  let minimumDistanceAlly = Infinity;

  for (let otherUnit of unitsArray) {
    if (otherUnit === unit || otherUnit.status === "dead") continue;

    const dist = unit.position.distanceTo(otherUnit.position);

    if (otherUnit.playerAlignment !== unit.playerAlignment && unit.canAttack === "both") {
      if (dist < minimumDistanceEnemy) {
        minimumDistanceEnemy = dist;
        nearestEnemy = otherUnit;
      }
    } else if (otherUnit.playerAlignment !== unit.playerAlignment && unit.canAttack === "ground" && otherUnit.airborne === "no" || otherUnit.playerAlignment !== unit.playerAlignment && unit.canAttack === "both" && otherUnit.airborne === "no") {
      if (dist < minimumDistanceEnemy) {
        minimumDistanceEnemy = dist;
        nearestEnemy = otherUnit;
      }
     } else if (otherUnit.playerAlignment !== unit.playerAlignment && unit.canAttack === "ground" && otherUnit.airborne === "yes") {
       continue; 
     }
     else {
      if (dist < minimumDistanceAlly) {
        minimumDistanceAlly = dist;
        nearestAlly = otherUnit;
      }
    }
  }

  return [nearestEnemy, nearestAlly];
}

/* movementAttackController does the Lion's share of the heavy lifting with unit behaviour, decding when a unit should move,
how far, whether it should attack etc
*/

function movementAttackController () {
    for (let unit of activeUnits) {

        // if the unit isn't dead, proceed to move / attack
        if (unit.status === "alive") {
        
        /* move and attack logic is a series of (mostly binary) decisions made in order:
        - if the unit has a target but the unit's target is dead and its attack is still running - stop attacking
        - if the unit's target isn't the same as the most recently calculated enemy, target the new enemy
        etc etc
        */

        if(unit.target) {
          if(unit.target.status === "dead" && unit._attackInterval) {
            
            clearInterval(unit._attackInterval);
          }
        }

        const nearestEnemyAndAlly = findNearestEnemyAndAlly(unit, activeUnits);
        if (unit.target != nearestEnemyAndAlly[0]) {
          unit.lastTarget = unit.target;
          unit.target = nearestEnemyAndAlly[0];
        }
        
        // if there are no units to attack, unit should not move or attack

        if (!nearestEnemyAndAlly[0]) continue;
        
        // define constants direction and distance, direction being a vector from unit to its target

            const enemyDirection = new THREE.Vector3().subVectors(unit.target.position, unit.position);
            unit.targetDirection = enemyDirection;
            const distance = enemyDirection.length();
          
        
        // if the unit hasn't got a target or its current target is dead then assign nearest enemy to the unit's target property
        if(!unit.target || unit.target.status === "dead") { 
            unit.lastTarget = unit.target;       
            unit.target = nearestEnemyAndAlly[0]     
        }

        // Calculate desired angle to target (radians)
        const angle = Math.atan2(enemyDirection.x, enemyDirection.z) + (unit.playerAlignment === "player" ? Math.PI : 0);

        // Get current facing angle (radians), wrapped to [-PI, PI]
        let currentAngle = ((unit.mesh.rotation.y + Math.PI) % (2 * Math.PI)) - Math.PI;

        // Calculate shortest signed angle difference (-PI to PI)
        let angleDifference = ((angle - currentAngle + Math.PI) % (2 * Math.PI)) - Math.PI;

        // If not facing target, turn toward it
        if (Math.abs(angleDifference) > THREE.MathUtils.degToRad(1)) { 

        // Turn by up to 1 degree per frame (converted to radians)
        let turnStep = Math.sign(angleDifference) * Math.min(Math.abs(angleDifference), THREE.MathUtils.degToRad(unit.turningSpeed));
        unit.mesh.rotation.y += turnStep;

        // Wrap rotation after update
        unit.mesh.rotation.y = ((unit.mesh.rotation.y + Math.PI) % (2 * Math.PI)) - Math.PI;
        } else {
        // Snap to target angle, wrapped
        unit.mesh.rotation.y = ((angle + Math.PI) % (2 * Math.PI)) - Math.PI;
        }


          
              // if the unit is too near to another unit, move further away to prevent stacking and bunching
              
              const nearestAlly = nearestEnemyAndAlly[1];

              // check that nearestAlly isn't null, for instance if there is only one unit left

              if (nearestAlly){
              const allyDirection = new THREE.Vector3().subVectors(unit.position, nearestAlly.position);
              const allyDistance = allyDirection.length();

              // only move if the distance between nearest allies is less than both unit's size and unit is in transit

              if (allyDistance <= unit.size + unit.target.size && distance > unit.range) {
                allyDirection.normalize();
                    unit.position.addScaledVector(allyDirection, unit.speed / 1.5);
                    unit.mesh.position.copy(unit.position);
              }
            }

            // if the distance between unit and target is greater than the unit's range, then move position closer to target
            
            if (distance > unit.range) {
                
                    enemyDirection.normalize();
                    unit.position.addScaledVector(enemyDirection, (0.02));
                    unit.mesh.position.copy(unit.position);
                    if (unit.name === 'ratTank' && !unit.animationActionStash.attack.isRunning()) {
                      unit.playAnimation('movement');
                    }  else if (unit.name != 'ratTank') {
                      unit.playAnimation('movement');
                    }
            }   
            
            
             // If the target has changed, clear the interval (stop attacking)
          if (unit.lastTarget !== nearestEnemyAndAlly[0]) {
             if (unit._attackInterval) {
              
              clearInterval(unit._attackInterval);
              unit._attackInterval = null;
            }
          unit.lastTarget = nearestEnemyAndAlly[0];
          
          }

          // If in range and facing, start attack interval if not running
          if (distance <= unit.range && Math.abs(angleDifference) < THREE.MathUtils.degToRad(unit.fieldOfView)) {
              if (!unit._attackInterval) {
              unit.attack();
              }
          }
          const found = activeUnits.find((element) => element.name === "ratTank");
          
        }
    }
}

// raycaster and mousedown event used for clicking interactions where the player is placing units. Essentially the 
// 2D array indeces of placementgrid array storing unit placement match the x and z coordinates of each plane in the grid exactly
// making it easy to use the x and z coordinates to add units to the array and invoke addUnit

const raycaster = new THREE.Raycaster();

 function onMouseDown(event) {
    const coords = new THREE.Vector2(
      (event.clientX / renderer.domElement.clientWidth) * 2 - 1,
      - ((event.clientY / renderer.domElement.clientHeight) * 2 - 1),
    );
    
  raycaster.setFromCamera(pointer, camera);
  // Raycast
  const intersections = raycaster.intersectObjects(displayedGridMeshes, true);
  if (intersections.length > 0 && selectedShopButton) {
    if (intersections[0].object.geometry.type === "PlaneGeometry") {
      intersections[0].object.visible = true;
    }
    {}
    if (currentFunds >= selectedShopButton.cost) {
    addUnit(selectedShopButton.name, "player", intersections[0].object.position.x, intersections[0].object.position.z);
    const i = Math.round(intersections[0].object.position.z * -1);
    const j = Math.round(intersections[0].object.position.x);
    placementBoard[i][j] = selectedShopButton.name;
    
    currentFunds = currentFunds - selectedShopButton.cost;
    updateFundsDisplay();
    selectedShopButton = null;
    } else {
      showFundsWarning(`Not enough funds for ${selectedShopButton.name}!`);
      intersections[0].object.visible = false;
      selectedShopButton = null;
    }
  }
  }

   


function placementRaycaster() {

if (placementRaycasterActive) return;
  placementRaycasterActive = true;

 window.addEventListener('mousedown', onMouseDown);
 
 
}

// simple button making function to prevent repeated code

function buttonMaker (width, height, text, onClick, options = {}) {
  const btn = document.createElement('button');
  btn.textContent = text;
  btn.style.width = options.width || width;
  btn.style.height = options.height || height;
  btn.style.fontSize = options.fontSize || 'clamp(0.6rem, 1vw, 1.2vh)';
  btn.style.borderRadius = options.borderRadius || '8px';
  btn.style.border = 'none';
  btn.style.background = options.background || '#2d7be0';
  btn.style.color = options.color || 'white';
  btn.style.cursor = 'pointer';
  btn.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
  btn.style.transition = 'background 0.2s';
  btn.onmouseenter = () => btn.style.background = options.hoverBackground || '#1756a9';
  btn.onmouseleave = () => btn.style.background = options.background || '#2d7be0';
  btn.addEventListener('click', onClick);
  return btn;
}

function addShopButtons () {
  for (let i = 0; i < currentShopStock.length; i++) {
  const unit = currentShopStock[i];
  const btn = buttonMaker(
    '8.6vw',
    '11.8vh',
    `${unit.name} - ${unit.cost} - ${unit.airVsGround} unit - can attack ${unit.canAttack}`,
    () => {
    selectedShopButton = unit;
    floatingCursor.src = `Assets/Textures/cursor-icons/${unit.name}.png`; 
    floatingCursor.style.display = 'block'; 
   
}
  );

  btn.style.position = 'fixed';
  btn.style.right = '30px';
  btn.style.top = `${400 + (i * 200)}px`;
  btn.style.zIndex = '2001';
  btn.style.display = 'flex';
  btn.style.flexDirection = 'column'; 
  btn.style.alignItems = 'center';
  btn.style.justifyContent = 'center';

  // Image centered inside button
  const img = document.createElement('img');
  img.src = `Assets/Textures/shop-buttons/${unit.name}.png`;
  img.style.width = '160px';
  img.style.height = '100px';
  img.style.pointerEvents = 'none';

  btn.appendChild(img);

  shopButtons.push(btn);
  document.body.appendChild(btn);

}

document.addEventListener('mousedown', function(e) {
  if (!shopButtons.some(btn => btn.contains(e.target))) {
    floatingCursor.style.display = 'none'; // Hide the cursor image
  }
});

}

function showFundsWarning(message) {
  let warningDiv = document.getElementById('funds-warning');
  if (!warningDiv) {
    warningDiv = document.createElement('div');
    warningDiv.id = 'funds-warning';
    warningDiv.style.position = 'fixed';
    warningDiv.style.top = '50%';
    warningDiv.style.left = '50%';
    warningDiv.style.transform = 'translate(-50%, -50%)';
    warningDiv.style.background = 'rgba(255, 80, 80, 0.95)';
    warningDiv.style.color = 'white';
    warningDiv.style.fontSize = '2rem';
    warningDiv.style.padding = '24px 48px';
    warningDiv.style.borderRadius = '16px';
    warningDiv.style.zIndex = '3000';
    warningDiv.style.boxShadow = '0 2px 16px rgba(0,0,0,0.2)';
    document.body.appendChild(warningDiv);
  }
  warningDiv.textContent = message;
  warningDiv.style.display = 'block';
  setTimeout(() => {
    warningDiv.style.display = 'none';
  }, 2000); // Hide after 2 seconds
}

function enemyPlacementController (){
  
  let depthOfPlacement = [];
  const zeroToTwo = Math.floor(Math.random()*2.99)
  switch(zeroToTwo) {
    case 0: depthOfPlacement = [20, 27];
    break;
    case 1: depthOfPlacement = [27, 33];
    break;
    case 2: depthOfPlacement = [33, boardDepth];
  }

  for (let i = depthOfPlacement[0]; i < depthOfPlacement[1]; i++) {
  for (let j = 0; j < boardWidth; j++)  {
    
    if (Math.random() > 0.98 && placementBoard[i][j] == "empty" && opponentFunds >= 50) {
      hiddenUnitsPlacementBoard[i][j] = "ratChaff";
      opponentFunds -= 50;
      enemyUnitsPreview.push("ratChaff")
  } else if (Math.random() <0.01 && placementBoard[i][j] == "empty" && opponentFunds >= 150  && currentGameRound > 1) {
      hiddenUnitsPlacementBoard[i][j] = "ratTank";
      opponentFunds -= 150;
      enemyUnitsPreview.push("ratTank")
    } else if (Math.random() <0.01 && placementBoard[i][j] == "empty" && opponentFunds >= 125 && currentGameRound > 3)   {
      hiddenUnitsPlacementBoard[i][j] = "ratBat";
      opponentFunds -= 125;
      enemyUnitsPreview.push("ratBat")
    }
}
}


};

function clearHiddenUnitsPlacementBoard() {
  for (let i = 0; i < hiddenUnitsPlacementBoard.length; i++) {
    for (let j = 0; j < hiddenUnitsPlacementBoard[i].length; j++) {
      if (hiddenUnitsPlacementBoard[i][j] !== "empty") {
        placementBoard[i][j] = hiddenUnitsPlacementBoard[i][j];
        hiddenUnitsPlacementBoard[i][j] = "empty";
      }
    }
  }
}



function roundResolveAlert(winner, loser, healthLost, draw, drawHealthLost) {
  
  console.log(roundResolved);
  console.log(playerHealth);
  console.log(opponentHealth);

  if (roundResolved) return;
  roundResolved = true;

  let resolveAlertDiv = document.getElementById('resolve-alert');
  if (!resolveAlertDiv) {
    resolveAlertDiv = document.createElement('div');
    resolveAlertDiv.id = 'resolve-alert';
    resolveAlertDiv.style.position = 'fixed';
    resolveAlertDiv.style.top = '50%';
    resolveAlertDiv.style.left = '50%';
    resolveAlertDiv.style.transform = 'translate(-50%, -50%)';
    resolveAlertDiv.style.background = 'rgba(255, 80, 80, 0.95)';
    resolveAlertDiv.style.color = 'white';
    resolveAlertDiv.style.fontSize = '2rem';
    resolveAlertDiv.style.padding = '24px 48px';
    resolveAlertDiv.style.borderRadius = '16px';
    resolveAlertDiv.style.zIndex = '3000';
    resolveAlertDiv.style.boxShadow = '0 2px 16px rgba(0,0,0,0.2)';
    document.body.appendChild(resolveAlertDiv);
  }
  if (playerHealth < 1 || opponentHealth < 1) {
      resolveAlertDiv.fontSize = '4rem'
      resolveAlertDiv.textContent = `${winner} wins the rat war! Game Over. Refresh the page to play again`;
  } else {

    if(playerHealth > 0 & opponentHealth > 0 && draw) {
      resolveAlertDiv.textContent = `DRAW! Player lost ${healthLost} health, Opponent lost ${drawHealthLost} health,`;
      resolveAlertDiv.style.display = 'block'
    } else {resolveAlertDiv.textContent = `${winner} wins! ${loser} lost ${healthLost} health.`;
  resolveAlertDiv.style.display = 'block';
    }
  

  let continueBtn = buttonMaker(
    100, 
    70, 
    "Continue",
    () => {
    currentGameRound++;
    currentPhaseIndex--;
    gamePhaseController();
    continueBtn.remove();
    resolveAlertDiv.remove();
    }
  );
  resolveAlertDiv.appendChild(continueBtn);
}

}

function unitInitialiser (board) {
    board.forEach((row, i) => {
  row.forEach((cell, j) => {
    
    let playerAlignment;
    if (i > 19) {
      playerAlignment = "opponent";
    } else {
      playerAlignment = "player";
    }

      if (cell != "empty") {
      addUnit(cell, playerAlignment, j, (i * -1));
};
    
  });
});
}

function unitPreviewInitialiser() {
  let previewBox = document.getElementById('enemy-units-preview');
  if (previewBox) previewBox.remove();

  // Create the preview box
  previewBox = document.createElement('div');
  previewBox.id = 'enemy-units-preview';
  previewBox.style.position = 'fixed';
  previewBox.style.top = '90px'; // Below health/timer/funds
  previewBox.style.left = '50%';
  previewBox.style.transform = 'translateX(-50%)';
  previewBox.style.background = 'rgba(80, 80, 80, 0.95)';
  previewBox.style.color = 'white';
  previewBox.style.fontSize = '1.5rem';
  previewBox.style.fontFamily = 'monospace';
  previewBox.style.padding = '24px 48px';
  previewBox.style.borderRadius = '16px';
  previewBox.style.zIndex = '2003';
  previewBox.style.boxShadow = '0 2px 16px rgba(0,0,0,0.2)';
  previewBox.style.display = 'flex';
  previewBox.style.flexDirection = 'column';
  previewBox.style.alignItems = 'center';
  previewBox.style.gap = '18px';

  // Add the header text
  const header = document.createElement('div');
  header.textContent = 'Enemy units deploying this round...';
  header.style.marginBottom = '12px';
  header.style.fontWeight = 'bold';
  previewBox.appendChild(header);

  // Add icons for each unit in enemyUnitsPreview
  const iconsRow = document.createElement('div');
  iconsRow.style.display = 'flex';
  iconsRow.style.gap = '12px';
  iconsRow.style.flexWrap = 'wrap';
  iconsRow.style.justifyContent = 'center';

  enemyUnitsPreview.forEach(unitName => {
    const icon = document.createElement('img');
    icon.src = `Assets/Textures/shop-buttons/${unitName}.png`;
    icon.alt = unitName;
    icon.style.width = '64px';
    icon.style.height = '40px';
    icon.style.objectFit = 'contain';
    icon.style.borderRadius = '6px';
    icon.style.background = 'rgba(255,255,255,0.1)';
    iconsRow.appendChild(icon);
  });

  previewBox.appendChild(iconsRow);

  document.body.appendChild(previewBox);
}

function boardUnitCleanUp () {
  
  scene.traverse(obj => {
    if (obj.isMesh && obj.geometry && obj.geometry.type != "PlaneGeometry") {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) {
        if (Array.isArray(obj.material)) {
          obj.material.forEach(mat => mat.dispose());
        } else {
          obj.material.dispose();
        }
      }
    }
  });
  for (const unit of activeUnits) {
    if (unit.mesh) {
      scene.remove(unit.mesh);
    }
  }

  activeUnits.length = 0;

}

function updateHealthDisplays() {
  playerHealthDisplay.textContent = `Player Health: ${playerHealth}`;
  opponentHealthDisplay.textContent = `Opponent Health: ${opponentHealth}`;
}

function stopAllAttacks () {
  for (let unit of activeUnits) {
    if (unit._attackInterval) {
      console.log(`clearing attack interval via stopAllAttacks! ${this.name}`);
    clearInterval(unit._attackInterval)
    unit._attackInterval = null;
    }
  }
}

function removeEnemyUnitsPreview() {
  const previewBox = document.getElementById('enemy-units-preview');
  if (previewBox) {
    previewBox.remove();
  }
}

function addStartBattleButton() {
  startBattleButtonContainer = document.createElement('div');
startBattleButtonContainer.style.position = 'fixed';
startBattleButtonContainer.style.left = '50%';
startBattleButtonContainer.style.bottom = '30px'; // 30px from the bottom
startBattleButtonContainer.style.transform = 'translateX(-50%)';
startBattleButtonContainer.style.display = 'flex';
startBattleButtonContainer.style.flexDirection = 'column';
startBattleButtonContainer.style.gap = '20px';
startBattleButtonContainer.style.zIndex = '1001';

const btn = document.createElement('button');
  btn.textContent = `Start Battle`;
  btn.style.width = '300px';
  btn.style.height = '100px';
  btn.style.fontSize = '1.1rem';
  btn.style.borderRadius = '8px';
  btn.style.border = 'none';
  btn.style.background = '#2d7be0';
  btn.style.color = 'white';
  btn.style.cursor = 'pointer';
  btn.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
  btn.style.transition = 'background 0.2s';
  btn.onmouseenter = () => btn.style.background = '#1756a9';
  btn.onmouseleave = () => btn.style.background = '#2d7be0';
  btn.addEventListener(
    "click", () => {
    currentPhaseIndex = 1;
    gamePhaseController();
}
);

  startBattleButtonContainer.appendChild(btn);
  document.body.appendChild(startBattleButtonContainer);
}

function createShadow(unit) {
  const shadowTexture = new THREE.TextureLoader().load('Assets/Textures/shadow/shadow.png');
  const shadowMaterial = new THREE.MeshBasicMaterial({ map: shadowTexture, transparent: true });
  const shadowPlane = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), shadowMaterial);
  shadowPlane.position.set(0, 0.01 + Math.random() * 0.01, 0); // Slightly above ground, random offset
  shadowPlane.rotation.set(degToRad(-90), 0, 0);
  shadowPlane.scale.set(unit.shadowScale, unit.shadowScale, 1); 
  return shadowPlane;
}

// Function to update funds display

function updateFundsDisplay() {
  fundsDisplay.textContent = `Funds: ${currentFunds}`;
}