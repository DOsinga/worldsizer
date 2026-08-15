class CartogramPlayer {
    constructor(canvas, geometry, options) {
        this.canvas = canvas;
        this.geometry = geometry;
        this.options = options || {};
        this.points = geometry.points.map(point => point.slice());
        this.animation = null;
        this.resolveAnimation = null;
        this.colors = {
            'Africa': '#D03030',
            'Europe': '#7E5E58',
            'Americas': '#00CC00',
            'Asia': '#3030DC',
            'Antarctica': '#AF00AF',
            'Oceania': '#00AFAF',
            'Seven seas (open ocean)': '#AFAF00'
        };
    }

    static scaledPoints(points, scale) {
        return points.map(point => [point[0] / scale, point[1] / scale]);
    }

    static decodePaths(dataset, basePoints) {
        const paths = {};
        for (const [name, encodedFrames] of Object.entries(dataset.paths)) {
            let previous = basePoints.map(point => [
                Math.round(point[0] * dataset.scale),
                Math.round(point[1] * dataset.scale)
            ]);
            paths[name] = encodedFrames.map(encoded => {
                const current = previous.map((point, index) => [
                    point[0] + encoded[index * 2],
                    point[1] + encoded[index * 2 + 1]
                ]);
                previous = current;
                return CartogramPlayer.scaledPoints(current, dataset.scale);
            });
        }
        return paths;
    }

    setPoints(points) {
        this.cancel();
        this.points = points.map(point => point.slice());
        this.draw();
    }

    cancel() {
        if (this.animation !== null) {
            cancelAnimationFrame(this.animation);
            this.animation = null;
        }
        if (this.resolveAnimation) {
            const resolve = this.resolveAnimation;
            this.resolveAnimation = null;
            resolve(false);
        }
    }

    async animateSequence(frames, millisecondsPerFrame) {
        this.cancel();
        for (const frame of frames) {
            if (!await this.animate(frame, millisecondsPerFrame)) return false;
        }
        return true;
    }

    animateTo(target, duration) {
        this.cancel();
        return this.animate(target, duration);
    }

    animate(target, duration) {
        const start = this.points.map(point => point.slice());
        const started = performance.now();
        return new Promise(resolve => {
            this.resolveAnimation = resolve;
            const step = now => {
                const progress = Math.min(1, (now - started) / duration);
                const eased = progress * progress * (3 - 2 * progress);
                this.points = start.map((point, index) => [
                    point[0] + (target[index][0] - point[0]) * eased,
                    point[1] + (target[index][1] - point[1]) * eased
                ]);
                this.draw();
                if (progress < 1) {
                    this.animation = requestAnimationFrame(step);
                } else {
                    this.animation = null;
                    this.resolveAnimation = null;
                    resolve(true);
                }
            };
            this.animation = requestAnimationFrame(step);
        });
    }

    draw() {
        const context = this.canvas.getContext('2d');
        const transform = this.transform();
        const excluded = new Set(this.options.exclude || []);
        context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        context.strokeStyle = '#303030';

        for (const country of this.geometry.countries) {
            if (excluded.has(country.cc)) continue;
            context.fillStyle = this.colors[country.continent];
            for (const shape of country.shapes) {
                context.beginPath();
                const last = transform(this.points[shape.pts[shape.pts.length - 1]]);
                context.moveTo(last[0], last[1]);
                for (const index of shape.pts) {
                    const point = transform(this.points[index]);
                    context.lineTo(point[0], point[1]);
                }
                context.fill();
                context.stroke();
            }
        }
    }

    transform() {
        if (!this.options.fit) {
            const zoom = this.options.zoom || 1;
            const xMargin = this.options.xMargin || 0;
            const yMargin = this.options.yMargin || 0;
            const height = this.canvas.height - yMargin * 2;
            return point => [
                zoom * point[0] * this.canvas.width + xMargin,
                zoom * point[1] * height + yMargin
            ];
        }

        const margin = this.options.margin || 0;
        const xs = this.points.map(point => point[0]);
        const ys = this.points.map(point => point[1]);
        const minX = Math.min(...xs);
        const minY = Math.min(...ys);
        const width = Math.max(...xs) - minX;
        const height = Math.max(...ys) - minY;
        return point => [
            (point[0] - minX) * this.canvas.width / width,
            (point[1] - minY) * (this.canvas.height - margin * 2) / height + margin
        ];
    }
}
