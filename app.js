var Rectangle = /** @class */ (function () {
    function Rectangle(x1, y1, x2, y2, color) {
        this.x1 = x1;
        this.x2 = x2;
        this.y1 = y1;
        this.y2 = y2;
        this.color = color;
    }
    return Rectangle;
}());
var Image_svg = /** @class */ (function () {
    function Image_svg(name) {
        this.rectangles = [];
        this.name = name;
    }
    Image_svg.prototype.getName = function () {
        return this.name;
    };
    Image_svg.prototype.getRectangles = function () {
        return this.rectangles;
    };
    Image_svg.prototype.addRectangles = function (rect) {
        for (var _i = 0, rect_1 = rect; _i < rect_1.length; _i++) {
            var r = rect_1[_i];
            this.rectangles.push(r);
        }
        return this;
    };
    Image_svg.prototype.setRectangles = function (rect) {
        this.rectangles = rect;
    };
    Image_svg.prototype.delRectangle = function (rect) {
        var index = this.rectangles.indexOf(rect, 0);
        if (index > -1) {
            this.rectangles.splice(index, 1);
        }
    };
    return Image_svg;
}());

var selectedRectangle = null;
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var isDrawing = false;
var startX = 0;
var startY = 0;
var image = new Image_svg("Canvas");

canvas.addEventListener('mousedown', function (e) {
    startX = e.offsetX;
    startY = e.offsetY;
    isDrawing = true;

});

canvas.addEventListener('mouseup', function (e) {
    if (isDrawing) {
        var x1 = startX;
        var y1 = startY;
        var x2 = e.offsetX;
        var y2 = e.offsetY;
        var color = document.getElementById('color').value;
        if (x1!=x2 && y1!=y2) image.addRectangles([new Rectangle(x1, y1, x2, y2, color)]);
        isDrawing = false;
        drawRectangles();
    }
});
canvas.addEventListener('click', function (e) {
    var x = e.offsetX;
    var y = e.offsetY;
    selectedRectangle = null;
    for (var _i = 0, _a = image.getRectangles(); _i < _a.length; _i++) {
        var rect = _a[_i];
        if (x >= rect.x1 && x <= rect.x2 && y >= rect.y1 && y <= rect.y2) {
            selectedRectangle = rect;
            break;
        }
    }
    updateSelectedRectangleInfo();
});
document.getElementById('add-rect').addEventListener('click', function () {
    var x1 = parseInt(document.getElementById('x1').value);
    var y1 = parseInt(document.getElementById('y1').value);
    var x2 = parseInt(document.getElementById('x2').value);
    var y2 = parseInt(document.getElementById('y2').value);
    var color = document.getElementById('color').value;
    image.addRectangles([new Rectangle(x1, y1, x2, y2, color)]);
    drawRectangles();
});

document.getElementById('delete-rect').addEventListener('click', function () {
    if (selectedRectangle) {
        image.delRectangle(selectedRectangle);
        selectedRectangle = null;
        drawRectangles();
        updateSelectedRectangleInfo();
    }
});
document.getElementById('save').addEventListener('click', save_image);

async function save_image() {
    try {
        let response = await fetch('http://localhost:8000/save_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(image)
        });
        let data = await response.json();
    } catch (error) {
        console.error('Error:', error);
    }

}


document.addEventListener("DOMContentLoaded", () => {
    const imageContainer = document.getElementById("image-container");

    function createImageBox() {
        const imageBox = document.createElement("div");
        imageBox.className = "image-box";
        const spinner = document.createElement("div");
        spinner.className = "spinner";
        imageBox.appendChild(spinner);
        return imageBox;
    }

    async function getLength() {
        try {
            const response = await fetch('http://127.0.0.1:8000/length/');
            if (!response.ok) {
                throw new Error("Failed to fetch images");
            }
            const data = await response.json();

            return data
        } catch (error) {
            console.error(error);
        }
    }

    function renderImages() {
        const max = 10;
        for (let i = 1; i <= max; i++) {
            const imageBox = createImageBox();
            imageContainer.appendChild(imageBox);
            renderImage(i, imageBox)
        }
    }

    async function renderImage(id, imageBox) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/picture_from_database/${id}/`);
            if (!response.ok) {
                throw new Error("Failed to fetch images");
            }
            const imageData = await response.json();
            const svgContainer = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            for (let rect of imageData.rectangles) {
                let newRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
                gsap.set(newRect, {
                attr: {
                    x: Math.min(rect.x1, rect.x2)/3,
                    y: Math.min(rect.y1, rect.y2)/3,
                    width: Math.abs(rect.x2-rect.x1)/3,
                    height: Math.abs(rect.y2-rect.y1)/3,
                    fill: rect.color,
                    class: "target"
                }
                });
                svgContainer.appendChild(newRect);
            }
            imageBox.innerHTML = '';
            imageBox.appendChild(svgContainer);
            return
        } catch (error) {
            const e = document.createElement("div");
            e.innerHTML = "Error&nbsp;&nbsp;";
            const button = document.createElement("BUTTON");
            button.onclick = function() { renderImage(id, imageBox); };
            button.textContent = "Reload"
            imageBox.innerHTML = " ";
            imageBox.append(e, button);
            console.log(imageBox.innerHTML);
            return
        }

     }
    renderImages()

})
function drawRectangles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (var i = 0, _a = image.getRectangles(); i < _a.length; i++) {
        var rect = _a[i];
        ctx.fillStyle = rect.color;
        ctx.fillRect(rect.x1, rect.y1, rect.x2 - rect.x1, rect.y2 - rect.y1);
    }

}
function updateSelectedRectangleInfo() {
    var infoDiv = document.getElementById('selected-rectangle-info');
    if (selectedRectangle) {
        infoDiv.textContent = "Selected Rectangle: (".concat(selectedRectangle.x1, ", ").concat(selectedRectangle.y1, ", ").concat(selectedRectangle.x2, ", ").concat(selectedRectangle.y2, ")");
    }
    else {
        infoDiv.textContent = 'No rectangle selected';
    }

}
drawRectangles();

