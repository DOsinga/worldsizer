function WorldSizer(baseState, countries) {
    this.baseState = baseState;
    this.iterations = [baseState];
    this.multipliers = [];
    this.countries = countries;
    return this;
}

WorldSizer.prototype = {
    setTargetWeights: function (targetWeights) {
        var continentWeights = {};
        var continentTargets = {};
        for (var cj = 0; cj < this.countries.length; cj++) {
            var tw = targetWeights[this.countries[cj].cc];
            if (tw) {
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
            if (targetWeights[this.countries[ci].cc]) {
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

    draw: function (canvas) {
        coos_for_pts = this.currentState();
        var context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.strokeStyle = '#303030';
        for (var ci = 0; ci < this.countries.length; ci++) {
            context.fillStyle = this.DEFAULT_COLORS[this.countries[ci].continent];
            for (var si = 0; si < this.countries[ci].shapes.length; si++) {
                var shape = this.countries[ci].shapes[si];
                context.beginPath();
                var last = coos_for_pts[shape.pts[shape.pts.length - 1]];
                context.moveTo(last[0] * canvas.width, last[1] * canvas.height);
                for (var i = 0; i < shape.pts.length; i++) {
                    var pt = coos_for_pts[shape.pts[i]];
                    context.lineTo(pt[0] * canvas.width, pt[1] * canvas.height);
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

    iterate: function () {
        var currentState = this.currentState();
        var deltas = [];
        for (ci = 0; ci < this.countries.length; ci++) {
            var country = this.countries[ci];
            var target = this.multipliers[ci];
            var targetSqrt = Math.sqrt(target);
            if (target == null) {
                target = 0.5;
            }
            for (var shi = 0; shi < country.shapes.length; shi++) {
                var shape = country.shapes[shi];

                var cenX = 0;
                var cenY = 0;
                var pti, pt;

                for (pti = 0; pti < shape.pts.length; pti++) {
                    pt = currentState[shape.pts[pti]];
                    cenX += pt[0];
                    cenY += pt[1];
                }
                cenX /= shape.pts.length;
                cenY /= shape.pts.length;

                var curSize = this.calcArea(shape.pts, currentState);
                var scale = Math.sqrt(curSize / shape.area);
                var ratio = targetSqrt / scale;

                var dXBridge = 0.0;
                var dYBridge = 0.0;
                if (shape.bridges.length) {
                    for (var bridge_idx = 0; bridge_idx < shape.bridges.length; bridge_idx++) {
                        var bridge = shape.bridges[bridge_idx];
                        var anchor = currentState[bridge[0]];
                        dXBridge += (anchor[0] - cenX) - bridge[1] * targetSqrt;
                        dYBridge += (anchor[1] - cenY) - bridge[2] * targetSqrt;
                    }
                }

                for (pti = 0; pti < shape.pts.length; pti++) {
                    var pt_index = shape.pts[pti];
                    pt = currentState[pt_index];
                    var curX = pt[0];
                    var curY = pt[1];

                    var pt0 = this.baseState[pt_index];

                    var shapeDX = cenX + targetSqrt * (pt0[0] - shape.x) - curX;
                    var shapeDY = cenY + targetSqrt * (pt0[1] - shape.y) - curY;

                    var dx = shapeDX;
                    var dy = shapeDY;

                    dx += dXBridge;
                    dy += dYBridge;

                    var delta = deltas[pt_index];
                    if (!delta) {
                        deltas[pt_index] = [dx, dy, 1 - ratio, 1];
                    } else {
                        deltas[pt_index] = [delta[0] + dx, delta[1] + dy, delta[2] + 1 - ratio, delta[3] + 1];
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
            var dX = curDelta[0] * curDelta[3] * curDelta[3];
            var dY = curDelta[1] * curDelta[3] * curDelta[3];
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

    MAX_SPEED: 0.0025,

    DEFAULT_COLORS: {
        'Africa': '#CC0000',
        'Europe': '#5E3E38',
        'Americas': '#00CC00',
        'Asia': '#0000CC',
        'Antarctica': '#AF00AF',
        'Oceania': '#00AFAF',
        'Seven seas (open ocean)': '#AFAF00'

    }
};