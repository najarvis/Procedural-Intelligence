function map_handler(map_w){
    this.tile_size = 32;
    this.tile_array_size = map_w;

    this.tiles = [];

    this.init = function() {
        for (var y = 0; y < this.tile_array_size; y++){
            for (var x = 0; x < this.tile_array_size; x++){
                type = ['grass', 'water'][x % 2 ^ y % 2]
                this.tiles.push(new tile(this, x * this.tile_size, y * this.tile_size, type));
            }
        }
        console.log(this.tiles);
    }

    this.init();

    this.draw = function() {
        for (var i = 0; i < this.tiles.length; i++){
            //console.log(current_tile);
            this.tiles[i].draw();
        }
    }

    this.update = function() {

    }
}

function tile(handler, x, y, type){
    this.handler = handler;

    this.x = x;
    this.y = y;

    this.width = this.handler.tile_size;
    this.pos = new vector(x, y);

    this.color = null;
    this.walkable = null;

    if (type == 'grass'){
        this.color = '#00ff00';
        this.walkable = true;

    } else if (type == 'water'){
        this.color = '#0000ff';
        this.walkable = false;
    }

    this.draw = function() {
        var ctx = gameSpace.context;
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.width, this.width);
    }
}
