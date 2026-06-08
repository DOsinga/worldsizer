function WorldSizer(baseState, countries) {
    this.baseState = baseState;
    this.iterations = [baseState];
    this.multipliers = [];
    this.countries = countries;
    this.country_codes = {}
    for (var i = 0; i < this.countries.length; i++) {
        this.country_codes[this.countries[i].cc] = 1;
    }
    return this;
}

WorldSizer.prototype = {
    setTargetWeights: function (targetWeights) {
        var continentWeights = {};
        var continentTargets = {};
        for (var cj = 0; cj < this.countries.length; cj++) {
            var tw = targetWeights[this.countries[cj].cc];
            if (tw !== undefined) {
                var continent = this.countries[cj].continent;
                if (!continentWeights[continent]) {
                    continentWeights[continent] = [];
                    continentTargets[continent] = [];
                }
                continentWeights[continent].push(this.countries[cj].weight);
                continentTargets[continent].push(tw);
            }
        }

        var continentMultipliers = {};
        for (var continentId in continentWeights) {
            if (continentWeights.hasOwnProperty(continentId)) {
                var tSum = 0.0;
                var oSum = 0.0;
                for (var kk = 0; kk < continentWeights[continentId].length; kk++) {
                    tSum += continentTargets[continentId][kk];
                    oSum += continentWeights[continentId][kk];
                }
                continentMultipliers[continentId] = tSum / oSum;
            }
        }

        this.multipliers = [];
        for (var ci = 0; ci < this.countries.length; ci++) {
            var m;
            if (targetWeights[this.countries[ci].cc] !== undefined) {
                m = targetWeights[this.countries[ci].cc] / this.countries[ci].weight;
            } else {
                m = continentMultipliers[this.countries[ci].continent];
                if (!m) {
                    if (this.countries[ci].continent == 'Antarctica') {
                        m = 0.0;
                    } else if (this.countries[ci].continent == 'Seven seas (open ocean)') {
                        m = continentMultipliers['Oceania'];
                    }
                }
            }
            this.multipliers.push(m);
        }
    },

    draw: function (canvas, margin) {
        if (!margin) {
            margin = 0;
        }
        var coos_for_pts = this.currentState();
        var xs = coos_for_pts.map(pt => pt[0]);
        var ys = coos_for_pts.map(pt => pt[1]);
        var min_x = Math.min.apply(Math, xs);
        var min_y = Math.min.apply(Math, ys);
        var max_x = Math.max.apply(Math, xs);
        var max_y = Math.max.apply(Math, ys);
        var x_size = max_x - min_x;
        var y_size = max_y - min_y;
        var context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.strokeStyle = '#303030';
        var height = canvas.height - margin * 2;
        for (var ci = 0; ci < this.countries.length; ci++) {
            context.fillStyle = this.DEFAULT_COLORS[this.countries[ci].continent];
            for (var si = 0; si < this.countries[ci].shapes.length; si++) {
                var shape = this.countries[ci].shapes[si];
                context.beginPath();
                var last = coos_for_pts[shape.pts[shape.pts.length - 1]];
                context.moveTo(
                    (last[0] - min_x) * canvas.width / x_size,
                    (last[1] - min_y) * height / y_size + margin
                );
                for (var i = 0; i < shape.pts.length; i++) {
                    var pt = coos_for_pts[shape.pts[i]];
                    context.lineTo(
                        (pt[0] - min_x) * canvas.width / x_size,
                        (pt[1] - min_y) * height / y_size + margin
                    );
                }
                context.fill();
                context.stroke();
            }
        }
    },

    currentState: function () {
        return this.iterations[this.iterations.length - 1];
    },

    calcArea: function (shape, index) {
        var n = shape.length;
        var area = 0;
        for (var i = 0; i < n; i++) {
            var j = (i + 1) % n;
            var pt_i = index[shape[i]];
            var pt_j = index[shape[j]];
            area += pt_i[0] * pt_j[1];
            area -= pt_j[0] * pt_i[1];
        }
        return Math.abs(area) / 2;
    },

    tick: function () {
        this.loss = 0.0;
        var currentState = this.currentState();
        var deltas = [];
        for (ci = 0; ci < this.countries.length; ci++) {
            var country = this.countries[ci];

            // The square root of the multiplier is a good thing to scale with:
            var targetSqrt = Math.sqrt(this.multipliers[ci]);
            for (var shi = 0; shi < country.shapes.length; shi++) {
                var shape = country.shapes[shi];

                // Find the center of the current shape:
                var curShapeCenterX = 0;
                var curShapeCenterY = 0;
                var pti, pt;

                for (pti = 0; pti < shape.pts.length; pti++) {
                    pt = currentState[shape.pts[pti]];
                    curShapeCenterX += pt[0];
                    curShapeCenterY += pt[1];
                }
                curShapeCenterX /= shape.pts.length;
                curShapeCenterY /= shape.pts.length;

                if (country.cc === 'us' && shi === 5) {
                    var xxx = country.cc;
                }

                // We have three forces:

                // Force 1: going home. All things equal this shape wants to migrate
                // where it was originally
                var dXHome = shape.x - curShapeCenterX;
                var dYHome = shape.y - curShapeCenterY;

                // Force 2: Bridges
                // Try to maintain the distance to outside points times the square root of the size target
                var dXBridge = 0.0;
                var dYBridge = 0.0;
                if (shape.bridges.length) {
                    for (var bridge_idx = 0; bridge_idx < shape.bridges.length; bridge_idx++) {
                        var bridge = shape.bridges[bridge_idx];
                        if (!this.country_codes[bridge[3]]) {
                            continue;
                        }
                        var anchor = currentState[bridge[0]];
                        dXBridge -= bridge[1] * targetSqrt - (anchor[0] - curShapeCenterX);
                        dYBridge -= bridge[2] * targetSqrt - (anchor[1] - curShapeCenterY);
                    }
                }

                // Calculate growSqrt for keeping the size:
                // Each point wants to maintain the (dx, dy) from the center of the shape times how much we need
                // to grow or shrink. Start with the ratio of the curren size vs the original size:
                var currentArea = this.calcArea(shape.pts, currentState);
                if (currentArea === 0 && this.multipliers[ci] === 0) {
                    // Target was 0, we are at 0, we're done (Antartica springs to mind):
                    continue;
                }
                var ratio = currentArea / shape.area;
                // And compare that with our goal multiplier. Take the square root since we are in 2D:
                var growSqrt = Math.sqrt(this.multipliers[ci] / ratio) - 1;

                before = this.loss;
                this.loss += Math.abs(growSqrt) * shape.area * this.multipliers[ci];
                if (!this.loss) {
                    console.log(this.loss, before);
                }

                for (pti = 0; pti < shape.pts.length; pti++) {

                    // Force 3: Keep the shape
                    // We want each point to maintain the (dx, dy) from the shapes center that is the same
                    // as it was, times the square root of the size multiplier:
                    var pt_index = shape.pts[pti];
                    var pt0 = this.baseState[pt_index];

                    var dXDesired = (pt0[0] - shape.x) * targetSqrt;
                    var dYDesired = (pt0[1] - shape.y) * targetSqrt;

                    pt = currentState[pt_index];
                    var dXActual = (pt[0] - curShapeCenterX);
                    var dYActual = (pt[1] - curShapeCenterY);

                    var dXShape = dXDesired - dXActual;
                    var dYShape = dYDesired - dYActual;

                    // Force 4: Target the size
                    // To target the size, move each point by growSqrt away (if positive) or to (if negative)
                    // the center of the shape:
                    var dxSize = dXActual * growSqrt;
                    var dySize = dYActual * growSqrt;

                    var dx = dxSize * 0.20 + dXShape + dXBridge * 20 + dXHome * 0.03;
                    var dy = dySize * 0.20 + dYShape + dYBridge * 20 + dYHome * 0.03;

//                    if (curY < 0.0) {
//                        dy -= curY * 0.05;
//                    }

                    var delta = deltas[pt_index];
                    if (!delta) {
                        deltas[pt_index] = [dx, dy];
                    } else {
                        deltas[pt_index] = [delta[0] + dx, delta[1] + dy];
                    }
                }
            }
        }

        res = [];
        for (var cc = 0; cc < currentState.length; cc++) {
            var curPt = currentState[cc];
            var curDelta = deltas[cc];
            if (curDelta == undefined) {
                res.push(curPt);
                continue;
            }
            var dX = curDelta[0];
            var dY = curDelta[1];
            var r2 = dX * dX + dY * dY;
            if (r2 > this.MAX_SPEED * this.MAX_SPEED) {
                var r = Math.sqrt(r2) / this.MAX_SPEED;
                dX /= r;
                dY /= r;
            }
            res.push([curPt[0] + dX,
                      curPt[1] + dY]);
        }
        this.iterations.push(res);
    },

    unWind: function () {
        this.iterations.pop();
    },

    MAX_SPEED: 0.002,

    DEFAULT_COLORS: {
        'Africa': '#D03030',
        'Europe': '#7E5E58',
        'Americas': '#00CC00',
        'Asia': '#3030DC',
        'Antarctica': '#AF00AF',
        'Oceania': '#00AFAF',
        'Seven seas (open ocean)': '#AFAF00'
    }
};
