const params = new URLSearchParams(window.location.search);
const playerName = params.get('playerName');
const sessionCode = params.get('sessionCode');

const socket = io.connect('https://to-farm-or-not-tofarm.onrender.com');

const config = {
    type: Phaser.AUTO,
    parent: 'gameWrapper',
    scene: {
        preload: preload,
        create: create,
        update: update
    },
    scale: {
        mode: Phaser.Scale.RESIZE,
        autoCenter: Phaser.Scale.CENTER_BOTH,
        width: '100%',
        height: '100%'
    },
    backgroundColor: '#ffff9f',
    antialias: false,
    render: {
        pixelArt: true
    },
};


//  This Scene has no aspect ratio lock, it will scale to fit the browser window, but will zoom to match the Game
class BackgroundScene extends Phaser.Scene
{
    gameScene;

    constructor ()
    {
        super('BackgroundScene');
    }

    preload ()
    {
        let assetRoot = '/to_farm_or_not_to_farm/assets/';
        this.load.spritesheet('button', assetRoot + 'button.png', { frameWidth: 204, frameHeight: 39 });
        this.load.image("lobbyContainer", assetRoot + "lobbyContainer.png");
    }

    create ()
    {
        const width = this.scale.gameSize.width;
        const height = this.scale.gameSize.height;

        this.scene.launch('GameScene');

        this.gameScene = this.scene.get('GameScene');
    }

    updateCamera ()
    {
        const width = this.scale.gameSize.width;
        const height = this.scale.gameSize.height;

        const camera = this.cameras.main;

        const zoom = this.gameScene.getZoom();

        camera.setZoom(zoom);
        camera.centerOn(972 / 2, (2160 / 2));

    }

}

//  This Scene is aspect ratio locked at 640 x 960 (and scaled and centered accordingly)
class GameScene extends Phaser.Scene
{
    GAME_WIDTH = 360;
    GAME_HEIGHT = 800;

    backgroundScene;
    parent;
    sizer;

    constructor ()
    {
        super('GameScene');
    }

    create () {
        const width = this.scale.gameSize.width;
        const height = this.scale.gameSize.height;

        this.parent = new Phaser.Structs.Size(width, height);
        this.sizer = new Phaser.Structs.Size(this.GAME_WIDTH, this.GAME_HEIGHT, Phaser.Structs.Size.FIT, this.parent);

        this.parent.setSize(width, height);
        this.sizer.setSize(width, height);

        this.backgroundScene = this.scene.get('BackgroundScene');

        this.updateCamera();

        this.scale.on('resize', this.resize, this);

        const guide = this.add.image(0, 0, 'guide').setOrigin(0, 0).setDepth(1).setVisible(false);

        this.add.text(this.GAME_WIDTH / 2, this.GAME_HEIGHT - 16, 'Press X to toggle mobile guide', {
            fontSize: '16px',
            fill: '#ffffff'
        }).setDepth(1).setOrigin(0.5);

        this.input.keyboard.on('keydown-X', () => {
            guide.visible = !guide.visible;
        });

        // Create your game objects and initialize game state
        let leaveGameButton = new uiWidgets.TextButton(this, 0, 0, "button", leaveGame, this, 0, 0, 1, 0)
            .setText("Leave Game", {
                fill: "black",
                fontFamily: "Righteous",
                fontSize: '24px', // Scale the font size
                antialias: false
            })
            .eventTextYAdjustment(1);

        let lobby = new uiWidgets.TextSprite(this, 38, 163, "lobbyContainer")
            .setText("",).setOrigin(0.0, 0.0);

        let column = new uiWidgets.Column(this, 0, 0);
        column.addNode(lobby, 0, 0);
        column.addNode(leaveGameButton, 182, 515);

    }

    resize (gameSize)
    {
        const width = gameSize.width;
        const height = gameSize.height;

        this.parent.setSize(width, height);
        this.sizer.setSize(width, height);

        this.updateCamera();
    }

    updateCamera ()
    {
        const camera = this.cameras.main;

        const x = Math.ceil((this.parent.width - this.sizer.width) * 0.5);
        const y = 0;
        const scaleX = this.sizer.width / this.GAME_WIDTH;
        const scaleY = this.sizer.height / this.GAME_HEIGHT;

        camera.setViewport(x, y, this.sizer.width, this.sizer.height);
        camera.setZoom(Math.max(scaleX, scaleY));
        camera.centerOn(this.GAME_WIDTH / 2, this.GAME_HEIGHT / 2);

        this.backgroundScene.updateCamera();
    }

    getZoom ()
    {
        return this.cameras.main.zoom;
    }


}
function leaveGame() {
    socket.emit('leave_game', {
        player_name: playerName,
        session_code: sessionCode
    });

    window.location.href = 'indexOLD.html';
}


const config = {
    type: Phaser.AUTO,
    backgroundColor: '#ffffff',
    scale: {
        mode: Phaser.Scale.RESIZE,
        parent: 'gameWrapper',
        width: 360,
        height: 800,
        min: {
            width: 360,
            height: 800
        },
        max: {
            width: 972,
            height: 2160
        }
    },
    scene: [ BackgroundScene, GameScene ],
};

const game = new Phaser.Game(config);
