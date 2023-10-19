import Handler from './to_farm_or_not_to_farm/src/scenes/handler.js'
import Title from './to_farm_or_not_to_farm/src/scenes/title.js'
import Preload from './to_farm_or_not_to_farm/src/scenes/preload.js'
import Hub from './to_farm_or_not_to_farm/src/scenes/hub.js'

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
    scene: [Handler, Hub, Preload, Title]

}

const game = new Phaser.Game(config)

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