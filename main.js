import Handler from './src/scenes/handler.js'
import Title from './src/scenes/title.js'
import Preload from './src/scenes/preload.js'
import Hub from './src/scenes/hub.js'
import Forecast from "./src/scenes/forecast.js";

// Aspect Ratio 16:9 - Portrait
const MAX_SIZE_WIDTH_SCREEN = 1920
const MAX_SIZE_HEIGHT_SCREEN = 1080
const MIN_SIZE_WIDTH_SCREEN = 270
const MIN_SIZE_HEIGHT_SCREEN = 480
const SIZE_WIDTH_SCREEN = 540
const SIZE_HEIGHT_SCREEN = 960

const params = new URLSearchParams(window.location.search);
export const playerName = params.get('playerName');
export const sessionCode = params.get('sessionCode');
console.log(playerName);
console.log(sessionCode);

const config = {
    type: Phaser.AUTO,
    scale: {
        mode: Phaser.Scale.RESIZE,
        parent: 'game',
        width: SIZE_WIDTH_SCREEN,
        height: SIZE_HEIGHT_SCREEN,
        min: {
            width: MIN_SIZE_WIDTH_SCREEN,
            height: MIN_SIZE_HEIGHT_SCREEN
        },
        max: {
            width: MAX_SIZE_WIDTH_SCREEN,
            height: MAX_SIZE_HEIGHT_SCREEN
        }
    },
    dom: {
        createContainer: true
    },
    scene: [Handler, Hub, Preload, Title, Forecast]

}

const game = new Phaser.Game(config)

// // Check if the Wake Lock API is available in the browser
// if ('wakeLock' in navigator) {
//     // Request a screen wake lock
//     async function requestWakeLock() {
//         try {
//             const wakeLock = await navigator.wakeLock.request('screen')
//             console.log('Screen wake lock activated:', wakeLock)
//         } catch (err) {
//             console.error('Failed to request a wake lock:', err)
//         }
//     }
//
//     // Request the wake lock when the page is focused
//     document.addEventListener('visibilitychange', () => {
//         if (document.visibilityState === 'visible') {
//             requestWakeLock()
//         }
//     })
// } else {
//     console.error('Wake Lock API is not supported in this browser.')
// }

// Global
game.debugMode = true
game.embedded = false // game is embedded into a html iframe/object

game.screenBaseSize = {
    maxWidth: MAX_SIZE_WIDTH_SCREEN,
    maxHeight: MAX_SIZE_HEIGHT_SCREEN,
    minWidth: MIN_SIZE_WIDTH_SCREEN,
    minHeight: MIN_SIZE_HEIGHT_SCREEN,
    width: SIZE_WIDTH_SCREEN,
    height: SIZE_HEIGHT_SCREEN
}

game.orientation = "portrait"
