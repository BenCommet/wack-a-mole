var w = 800;
var h = 600;
var game = new Phaser.Game(w, h, Phaser.AUTO, '', { preload: preload, create: create, update: update });

function preload() {
    game.load.spritesheet('upDown', 'assets/images/upDown.png', 45, 40, 16);


}

//Global Variables
var moleGroup;

function create() {
    game.stage.backgroundColor = "#66ff66";

    makeMoles();

}

function makeMoles(){
    moleGroup = game.add.group();
    mole = moleGroup.create(100, 100, 'upDown');
    mole.frame = 0;
    mole.animations.add('up', [0,1,2,3,4,5,6,7], 3, true);
    mole.animations.play('up');
    mole.scale.set(2);

    // for(var i = 0; i < 6; i++){
    //
    // }
}

function update() {

}
