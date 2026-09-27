import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

interface GlobeProps {
  onSelectRegion?: (regionId: string) => void;
  selectedRegion?: string | null;
}

export const Globe3D: React.FC<GlobeProps> = ({ onSelectRegion, selectedRegion }) => {
  const mountRef = useRef<HTMLDivElement>(null);
  // Keep the latest callback in a ref so the WebGL scene is built once, not on every parent render
  const onSelectRef = useRef(onSelectRegion);
  useEffect(() => {
    onSelectRef.current = onSelectRegion;
  }, [onSelectRegion]);

  useEffect(() => {
    const currentMount = mountRef.current;
    if (!currentMount) return;

    const width = currentMount.clientWidth;
    const height = currentMount.clientHeight;

    // Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.z = 220;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    currentMount.appendChild(renderer.domElement);

    // Earth Sphere
    const globeRadius = 80;
    const sphereGeo = new THREE.SphereGeometry(globeRadius, 48, 48);
    const sphereMat = new THREE.MeshPhongMaterial({
      color: 0x0a1628,
      emissive: 0x050c18,
      specular: 0x00d2ff,
      shininess: 15,
      wireframe: false,
    });
    const globe = new THREE.Mesh(sphereGeo, sphereMat);
    scene.add(globe);

    // Tactical Wireframe Overlay
    const wireGeo = new THREE.SphereGeometry(globeRadius + 0.5, 24, 24);
    const wireMat = new THREE.MeshBasicMaterial({
      color: 0x1e3a5f,
      wireframe: true,
      transparent: true,
      opacity: 0.25,
    });
    const wireSphere = new THREE.Mesh(wireGeo, wireMat);
    scene.add(wireSphere);

    // Atmospheric Glow Ring
    const haloGeo = new THREE.SphereGeometry(globeRadius + 4, 32, 32);
    const haloMat = new THREE.MeshBasicMaterial({
      color: 0x002395,
      transparent: true,
      opacity: 0.15,
      side: THREE.BackSide,
    });
    const haloMesh = new THREE.Mesh(haloGeo, haloMat);
    scene.add(haloMesh);

    // Hotspot Pins: Paris (FRA), UNHQ (USA), Middle East, Eastern Europe, Sahel
    const hotspots = [
      { id: "paris", name: "PARIS (HQ)", lat: 48.8566, lng: 2.3522, color: 0x00d2ff, isHQ: true },
      { id: "newyork", name: "UNHQ (NY)", lat: 40.7128, lng: -74.006, color: 0x4b92db, isHQ: true },
      { id: "middle-east", name: "CRISIS: LEVANT / RED SEA", lat: 33.8938, lng: 35.5018, color: 0xed2939, isHQ: false },
      { id: "eastern-europe", name: "CRISIS: BLACK SEA", lat: 48.3794, lng: 31.1656, color: 0xffa500, isHQ: false },
      { id: "sub-saharan-africa", name: "SECURITY: SAHEL", lat: 14.4974, lng: -14.4524, color: 0xd4af37, isHQ: false },
    ];

    const pinGroup = new THREE.Group();
    scene.add(pinGroup);

    hotspots.forEach((spot) => {
      const phi = (90 - spot.lat) * (Math.PI / 180);
      const theta = (spot.lng + 180) * (Math.PI / 180);
      const x = -(globeRadius * Math.sin(phi) * Math.cos(theta));
      const z = globeRadius * Math.sin(phi) * Math.sin(theta);
      const y = globeRadius * Math.cos(phi);

      // Pin Mesh
      const pinGeo = new THREE.SphereGeometry(spot.isHQ ? 2.5 : 3.5, 16, 16);
      const pinMat = new THREE.MeshBasicMaterial({ color: spot.color });
      const pinMesh = new THREE.Mesh(pinGeo, pinMat);
      pinMesh.position.set(x, y, z);
      pinMesh.userData = { id: spot.id, name: spot.name };
      pinGroup.add(pinMesh);

      // Ring pulse
      const ringGeo = new THREE.RingGeometry(spot.isHQ ? 3.5 : 4.5, spot.isHQ ? 4.5 : 5.8, 24);
      const ringMat = new THREE.MeshBasicMaterial({
        color: spot.color,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.6,
      });
      const ringMesh = new THREE.Mesh(ringGeo, ringMat);
      ringMesh.position.set(x * 1.01, y * 1.01, z * 1.01);
      ringMesh.lookAt(x * 2, y * 2, z * 2);
      pinGroup.add(ringMesh);
    });

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0x00d2ff, 1.2);
    dirLight1.position.set(150, 100, 100);
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0xed2939, 0.5);
    dirLight2.position.set(-150, -50, -50);
    scene.add(dirLight2);

    // Interactive Drag Rotation
    let isDragging = false;
    let prevMousePos = { x: 0, y: 0 };

    const onMouseDown = (e: MouseEvent) => {
      isDragging = true;
      prevMousePos = { x: e.clientX, y: e.clientY };
    };

    const onMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      const deltaX = e.clientX - prevMousePos.x;
      const deltaY = e.clientY - prevMousePos.y;

      globe.rotation.y += deltaX * 0.005;
      wireSphere.rotation.y += deltaX * 0.005;
      pinGroup.rotation.y += deltaX * 0.005;

      globe.rotation.x += deltaY * 0.005;
      wireSphere.rotation.x += deltaY * 0.005;
      pinGroup.rotation.x += deltaY * 0.005;

      prevMousePos = { x: e.clientX, y: e.clientY };
    };

    const onMouseUp = () => {
      isDragging = false;
    };

    const domElement = renderer.domElement;
    domElement.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);

    // Raycaster for Pin Click
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    const onClick = (e: MouseEvent) => {
      const rect = domElement.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(pinGroup.children);
      if (intersects.length > 0) {
        const hit = intersects[0].object;
        if (hit.userData && hit.userData.id && onSelectRef.current) {
          onSelectRef.current(hit.userData.id);
        }
      }
    };
    domElement.addEventListener('click', onClick);

    // Animation Loop
    let animationFrameId: number;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      if (!isDragging) {
        globe.rotation.y += 0.0015;
        wireSphere.rotation.y += 0.0015;
        pinGroup.rotation.y += 0.0015;
      }
      renderer.render(scene, camera);
    };
    animate();

    const handleResize = () => {
      if (!currentMount) return;
      const newW = currentMount.clientWidth;
      const newH = currentMount.clientHeight;
      camera.aspect = newW / newH;
      camera.updateProjectionMatrix();
      renderer.setSize(newW, newH);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animationFrameId);
      domElement.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      domElement.removeEventListener('click', onClick);
      window.removeEventListener('resize', handleResize);
      if (currentMount.contains(domElement)) {
        currentMount.removeChild(domElement);
      }
      renderer.dispose();
    };
  }, []);

  return (
    <div className="relative w-full h-full min-h-[420px] rounded-xl overflow-hidden bg-gradient-to-b from-[#050914] via-[#091326] to-[#040813] border border-slate-800 shadow-2xl flex items-center justify-center">
      <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />
      
      {/* Tactical HUD Overlay Elements */}
      <div className="absolute top-3 left-3 bg-slate-950/80 backdrop-blur-md px-3 py-1.5 rounded border border-cyan-500/30 text-xs font-mono text-cyan-400 flex items-center space-x-2">
        <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
        <span>UNSC GLOBAL TELEMETRY // ORBITAL VIEW</span>
      </div>

      <div className="absolute bottom-3 left-3 bg-slate-950/85 backdrop-blur-md p-2.5 rounded-lg border border-slate-700/60 text-[11px] font-mono space-y-1">
        <div className="flex items-center space-x-2 text-slate-300">
          <span className="w-2.5 h-2.5 rounded-full bg-[#00d2ff]" />
          <span>PARIS MISSION COMMAND (HQ)</span>
        </div>
        <div className="flex items-center space-x-2 text-slate-300">
          <span className="w-2.5 h-2.5 rounded-full bg-[#ed2939]" />
          <span>ACTIVE CRISIS HOTSPOT (CLICK PIN)</span>
        </div>
        <div className="flex items-center space-x-2 text-slate-300">
          <span className="w-2.5 h-2.5 rounded-full bg-[#4b92db]" />
          <span>UNITED NATIONS SECURITY COUNCIL (NY)</span>
        </div>
      </div>

      <div className="absolute top-3 right-3 text-right text-[10px] font-mono text-slate-400 bg-slate-950/70 p-2 rounded border border-slate-800">
        <div>LAT: 33.89° N | LNG: 35.50° E</div>
        <div>PROJECTION: WGS-84 TACTICAL</div>
        <div className="text-cyan-400">STATUS: LIVE FEED SYNCHRONIZED</div>
      </div>
    </div>
  );
};
