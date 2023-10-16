export default class Hub extends Phaser.Scene {

    // Vars
    handlerScene = null

    constructor() {
        super('hub')
    }

    preload() {
        // Images

        //---------------------------------------------------------------------->
        this.canvasWidth = this.sys.game.canvas.width
        this.canvasHeight = this.sys.game.canvas.height
        this.handlerScene = this.scene.get('handler')
        //Orientation
        this.scale.lockOrientation(this.game.orientation)

    }

    create() {        

        this.scale.on("resize", this.resize, this)
    }


    update() {
        if (this.handlerScene.sceneRunning === 'title') {

        } 
    }

    resize() {

    }
}