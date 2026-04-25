varying highp vec2 v_uv;
uniform highp float time;

// simple random
float rand(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

// smooth noise
float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);

    float a = rand(i);
    float b = rand(i + vec2(1.0, 0.0));
    float c = rand(i + vec2(0.0, 1.0));
    float d = rand(i + vec2(1.0, 1.0));

    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(a, b, u.x)
         + (c - a) * u.y * (1.0 - u.x)
         + (d - b) * u.x * u.y;
}

void main() {
    vec2 uv = v_uv;

    // smoke rises
    uv.y -= time * 0.15;

    // add turbulence
    float n = noise(uv * 6.0 + time * 0.2);

    // shape & fade
    float density = smoothstep(0.3, 0.8, n);
    density *= smoothstep(1.0, 0.2, v_uv.y);

    vec3 smokeColor = vec3(0.6, 0.6, 0.6);

    gl_FragColor = vec4(smokeColor, density * 0.6);
}