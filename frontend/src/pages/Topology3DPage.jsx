import React, { Suspense, useContext, useMemo } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Text, Line, Sphere } from '@react-three/drei';
import { TopologyContext } from '../contexts/TopologyContext';

const Node3D = ({ node }) => {
  const color = node.properties.status === 'online' ? '#3fb950' : '#f85149';
  return (
    <group position={node.position3d}>
      <Sphere args={[0.2, 32, 32]}>
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={2} toneMapped={false} />
      </Sphere>
      <Text position={[0, 0.4, 0]} fontSize={0.15} color="white" anchorX="center" anchorY="middle">
        {node.properties.label}
      </Text>
    </group>
  );
};

const Link3D = ({ startNode, endNode }) => {
  return <Line points={[startNode.position3d, endNode.position3d]} color="gray" lineWidth={1} />;
};

const Topology3DPage = () => {
  const { topology } = useContext(TopologyContext);

  const { nodesWith3DPos, links } = useMemo(() => {
    const nodes = topology.features.filter(f => f.geometry.type === 'Point');
    const nodesWith3DPos = nodes.map((node, i) => ({
        ...node,
        position3d: [(i % 6 - 3) * 3, Math.floor(i / 6) * -3, (i % 3 - 1) * 2],
    }));

    const nodeMap = Object.fromEntries(nodesWith3DPos.map(n => [n.properties.id, n]));
    const links = topology.features
        .filter(f => f.geometry.type === 'LineString')
        .map(link => ({
            ...link,
            startNode: nodeMap[link.properties.source],
            endNode: nodeMap[link.properties.target]
        }))
        .filter(l => l.startNode && l.endNode);

    return { nodesWith3DPos, links };
  }, [topology]);


  return (
    <div className="h-full w-full bg-noc-dark">
        <div className="absolute top-4 left-4 text-noc-text-secondary z-10 p-2 bg-noc-light-dark/50 rounded-md pointer-events-none">
            Experimentelle 3D-Ansicht. Nutzen Sie die Maus zum Navigieren.
        </div>
        <Canvas camera={{ position: [0, -2, 12], fov: 75 }}>
            <ambientLight intensity={1.5} />
            <pointLight position={[10, 10, 10]} intensity={2.5} />
            <Suspense fallback={null}>
              {nodesWith3DPos.map(node => <Node3D key={node.properties.id} node={node} />)}
              {links.map((link, i) => <Link3D key={i} {...link} />)}
            </Suspense>
            <OrbitControls />
        </Canvas>
    </div>
  );
};

export default Topology3DPage;