### A3D_(A⊙B)ⁿ

**Description**

Applies a selectable math operation to two values, then raises the result to a given exponent.

**Inputs**

- Operation `Menu` — Type of operation to perform
- A `Float` — First operand
- B `Float` — Second operand
- Exponent `Float` — Power the result is raised to

**Outputs**

- Value `Float` — Result of the operation raised to the exponent


### A3D_2D Line Cut

**Description**

Cuts a body mesh against a tool mesh's edges along a shared plane, returning the resulting mesh along with intersection status and position for each intersected element.

**Inputs**

- Body Mesh `Geometry` — Geometry to split
- Tool Mesh `Geometry` — Geometry that will perform the cut
- Selection `Boolean` — Which edges in body geometry to cut
- Cut Body `Boolean` — Insert new edge (cut)
- Tool Index `Integer` — Index of edge in tool body to be used

**Outputs**

- Mesh `Geometry` — Body mesh with the cut applied
- Intersected `Boolean` — True where the tool edge intersects the body
- Position `Vector` — Position of the intersection


### A3D_2D Navier Stokes Solver

**Description**

A 2D fluid solver operating on a grid, advecting velocity, pressure, density, and color fields with configurable damping and external force/collision input, for smoke and liquid style simulations.

**Inputs**

- Geometry `Geometry` — Grid geometry the simulation runs on
- Resolution `Integer` — Number of vertices in the X direction
- Scale `Float` — Scale of the simulation grid
- Damping `Float` — Amount the velocity is damped each step
- Velocity `Vector` — Velocity field of the fluid
- Pressure `Float` — Pressure field of the fluid
- Density `Float` — Density field of the fluid
- Color `Color` — Color field carried along by the fluid
- External `Boolean` — Enable interaction with an external object
- External Object `Object` — Object that interacts with the fluid
- External Dampening `Float` — How much to damp the velocity
- External Collision Proximity `Float` — Distance within which the external object affects the fluid

**Outputs**

- Geometry `Geometry` — Grid geometry with the updated simulation fields


### A3D_2D Shape Cut

**Description**

Cuts a body mesh using an arbitrary 2D tool mesh as the cutting shape, returning the cut mesh, intersection status, and intersection positions.

**Inputs**

- Cut Body `Boolean` — Insert vertex (cut) geometry
- Body Mesh `Geometry` — Geometry to be cut
- Body Selection `Boolean` — Limit affected edges
- Tool Mesh `Geometry` — Cutting geometry

**Outputs**

- Mesh `Geometry` — Body mesh with the cut applied
- Intersected `Boolean` — True where the tool mesh intersects the body
- Intersection Position `Vector` — Position of the intersection

### A3D_Active Camera Transform

**Description**

Returns the transform (and separately, location/rotation/scale) of the scene's active camera, with a mode switch for which representation to output.

**Inputs**

- Mode `Menu` — Which representation of the transform to output

**Outputs**

- Transform `Matrix` — Transformation matrix containing the location, rotation and scale of the camera
- Location `Vector` — Location of the active camera
- Rotation `Rotation` — Rotation of the active camera
- Scale `Vector` — Scale of the active camera


### A3D_Age Cull

**Description**

Deletes Geometry on the selected Domain when `age` is greater than or equal to `max_age`. Used with other Age* nodes.

**Inputs**

- Geometry `Geometry` — Geometry to remove expired elements from
- Selection `Boolean` — Elements that can be culled
- Domain `Menu` — Domain to cull on

**Outputs**

- Geometry `Geometry` — Geometry with expired elements removed


### A3D_Age Initialize

**Description**

Write the attribute `max_age` on the selected Domain. Used with other Age* nodes.

**Inputs**

- Geometry `Geometry` — Geometry to store the max_age attribute on
- Selection `Boolean` — Elements to initialize
- Domain `Menu` — Domain to store max_age on
- Max Age `Float` — Age at which an element is considered expired

**Outputs**

- Geometry `Geometry` — Geometry with the max_age attribute stored


### A3D_Age Update

**Description**

Increments the attribute `age` by input `Delta Time` on the selected Domain. Used with other Age* nodes.

**Inputs**

- Geometry `Geometry` — Geometry to update the age attribute on
- Selection `Boolean` — Elements to age
- Delta Time `Float` — Amount of time added to age
- Domain `Menu` — Domain the age attribute is stored on

**Outputs**

- Geometry `Geometry` — Geometry with the age attribute updated


### A3D_Angle Between Vectors

**Description**

Computes the angle in radians between two input vectors.

**Inputs**

- Vector A `Vector` — First vector
- Vector B `Vector` — Second vector

**Outputs**

- Radians `Float` — Angle between the vectors in radians


### A3D_Angle to Vector

**Description**

Converts a 2D angle (radians) into a unit direction vector.

**Inputs**

- Angle `Float` — Angle in radians

**Outputs**

- Vector `Vector` — Unit direction vector for the angle


### A3D_Axis Alignment

**Description**

Determines which world axis (X, Y, or Z) a given vector is most closely aligned to, within an epsilon tolerance, and outputs boolean results per axis.

**Inputs**

- Vector `Vector` — Direction Vector
- Epsilon `Float` — Comparison threshold

**Outputs**

- X `Boolean` — Aligned to X Axis
- Y `Boolean` — Aligned to Y Axis
- Z `Boolean` — Aligned to Z Axis


### A3D_Axis Picker

**Description**

A menu-driven axis picker that outputs a unit vector for the selected X, Y, or Z axis, with an invert option.

**Inputs**

- Axis `Menu` — Direction to Return
- Invert `Boolean` — Flip the direction of the returned axis

**Outputs**

- Vector `Vector` — Direction unit vector


### A3D_Aⁿ⊙Bⁿ

**Description**

Raises inputs A and B to a given exponent before combining them with a selectable math operation.

**Inputs**

- Operation `Menu` — Type of operation to perform
- A `Float` — First operand, raised to the exponent
- B `Float` — Second operand, raised to the exponent
- Exponent `Float` — Power A and B are raised to

**Outputs**

- Value `Float` — Result of the operation


### A3D_Ballistic Arc

**Description**

Computes the position and velocity of a point along a ballistic (projectile) trajectory at a given time, from an initial position, initial velocity, and gravity vector.

**Inputs**

- Initial Position `Vector` — Position at launch
- Initial Velocity `Vector` — Velocity at launch
- Gravity `Vector` — Gravity acceleration vector
- Time `Float` — Time elapsed since launch

**Outputs**

- Position `Vector` — Position at the given time
- Velocity `Vector` — Velocity at the given time


### A3D_Bell Curve

**Description**

Evaluates a Gaussian (normal distribution) bell curve for an input value, given a mean and standard deviation.

**Inputs**

- Value `Float` — Value to evaluate the curve at
- Mean `Float` — Center (peak) of the curve
- Standard Deviation `Float` — Width of the curve

**Outputs**

- Value `Float` — Height of the curve at the input value


### A3D_Boolean Grid Check

**Description**

Tests a boolean value against a rectangular sub-region (width/height) of a resolution-addressed grid at a given index.

**Inputs**

- Index `Integer` — Index of the grid cell the sub-region is positioned at
- Width `Integer` — Width of the sub-region in grid cells
- Height `Integer` — Height of the sub-region in grid cells
- Boolean `Boolean` — Boolean value to test
- Resolution `Integer` — Resolution of the grid

**Outputs**

- Boolean `Boolean` — Result of the test over the sub-region


### A3D_Bounce Reflect

**Description**

Reflects an incoming velocity off a plane defined by a normal, with restitution controlling bounce energy retention and friction damping the tangential component.

**Inputs**

- Incoming Velocity `Vector` — Velocity before the bounce
- Plane Normal `Vector` — Normal of the surface being bounced off
- Restitution `Float` — Fraction of energy kept after the bounce
- Friction `Float` — Damping applied to the tangential component

**Outputs**

- Reflected Velocity `Vector` — Velocity after the bounce


### A3D_Camera Cull

**Description**

Removes or masks geometry that falls outside a camera's view frustum, with padding and a minimum-distance cutoff, useful for render-time optimization.

**Inputs**

- Geometry `Geometry` — Geometry to cull
- Source `Menu` — Where the camera comes from
- Camera `Object` — Camera object to cull against
- Domain `Menu` — Which type of element to Cull
- Padding `Float` — Extend bounds of frustum beyond edge of screen
- Min Distance `Float` — Minimum distance after which to begin culling

**Outputs**

- Geometry `Geometry` — Geometry with out-of-view elements removed


### A3D_Camera FOV

**Description**

Returns the horizontal and vertical field of view of a camera, optionally defaulting to the active scene camera.

**Inputs**

- Use Active `Boolean` — Use the active scene camera
- Camera `Object` — Camera object to read the field of view from

**Outputs**

- Horizontal FOV `Float` — Horizontal field of view of the camera
- Vertical FOV `Float` — Vertical field of view of the camera


### A3D_Catenary Curve

**Description**

Relaxes a curve's selected control points into a catenary (hanging-chain) shape based on a stiffness parameter. Useful for cables, ropes, and chains.

**Inputs**

- Curve `Geometry` — Curve to relax into a catenary shape
- Selection `Boolean` — Control points to affect
- Stiffness `Float` — How rigid the hanging shape is

**Outputs**

- Curve `Geometry` — Curve with a catenary shape


### A3D_Cell Fracture

**Description**

Fractures input geometry into a set of instanced cell pieces using Voronoi-style cell partitioning, with controls for fracture scale/detail/gap, remeshing, and edge-wear seeding.

**Inputs**

- Geometry `Geometry` — Geometry to fracture
- Fracture Scale `Float` — Scale of Voronoi noise
- Fracture Detail `Float` — The scale of a Voronoi layer relative to that of the previous layer
- Fracture Gap `Float` — Spacing between cells
- Seed `Integer` — Random seed for the fracture pattern
- Remesh Mode `Menu` — How the geometry is remeshed before fracturing
- Remesh Voxel Size `Float` — Size of the voxels used when remeshing
- Remesh Accuracy `Integer` — Accuracy of the remesh
- Edge Wear Seed `Integer` — Random seed for the edge wear pattern

**Outputs**

- Instances `Geometry` — Fractured pieces as instances


### A3D_Circumcircle Test

**Description**

Determines whether a test point lies inside, on, or outside the circumcircle defined by three points.

**Inputs**

- Test Against `Menu` — Field method for circle origins
- Position `Vector` — Point to test
- Point A `Vector` — First triangle point
- Point B `Vector` — Second triangle point
- Point C `Vector` — Third triangle point

**Outputs**

- Determinant `Float` — Sign shows whether the point is inside, on, or outside the circumcircle


### A3D_Clamp Vector

**Description**

Clamps each component of a vector independently between corresponding min and max vectors.

**Inputs**

- Vector `Vector` — Vector to clamp
- Min `Vector` — Per-component minimum
- Max `Vector` — Per-component maximum

**Outputs**

- Vector `Vector` — Clamped vector


### A3D_Conform To Surface

**Description**

Snaps or projects a mesh's selected vertices onto a target surface mesh within a snapping distance, with an additional surface offset.

**Inputs**

- Mesh `Geometry` — Mesh to snap
- Selection `Boolean` — Vertices to snap
- Surface Mesh `Geometry` — Surface to snap to
- Snapping Distance `Float` — Maximum distance to search for the surface
- Surface Offset `Float` — Offset from the surface after snapping

**Outputs**

- Mesh `Geometry` — Mesh with vertices snapped to the surface


### A3D_Coordinate of Grid Index

**Description**

Converts a flat grid index into 2D (X, Y) coordinates for a grid of a given resolution. The inverse of Index of Grid Coordinate.

**Inputs**

- Resolution `Integer` — Resolution of the grid
- Index `Integer` — Flat index into the grid

**Outputs**

- X `Integer` — X coordinate in the grid
- Y `Integer` — Y coordinate in the grid


### A3D_Cotangent

**Description**

Computes the cotangent of an angle in radians.

**Inputs**

- Value `Float` — Angle in radians

**Outputs**

- Value `Float` — Cotangent of the angle


### A3D_Debug Vectors

**Description**

Generates arrow-like geometry that visualizes vectors, for debugging vector data.

**Inputs**

- Geometry `Geometry` — Points to draw the vectors at
- Vertices `Integer` — The number of vertices on the top and bottom circles
- Vector `Vector` — Vector to visualize
- Length `Float` — Length of the arrows
- Radius `Float` — Radius of the arrows

**Outputs**

- Geometry `Geometry` — Generated debug arrow geometry


### A3D_Deform To UV Surface

**Description**

Deforms a mesh to conform to a target surface using a UV-space transfer map, with an optional debug output for visualizing the mapping. Input Mesh be placed within a +1 unit bounding box on the XY plane.

**Inputs**

- Mesh `Geometry` — Surface to deform
- Transfer Surface `Object` — Surface to transfer to
- Transfer Map `String` — Name of the UV transfer map to use
- Debug `Boolean` — Show UV Space Geometry

**Outputs**

- Mesh `Geometry` — Mesh deformed onto the target surface


### A3D_Delaunay Triangulation

**Description**

Builds a Delaunay triangulation over the input geometry's points, with controls for minimum spacing, density falloff, boundary preservation, and inset.

**Inputs**

- Geometry `Geometry` — Points to triangulate
- Distance Min `Float` — Minimum spacing between points
- Density Max `Float` — Maximum point density
- Density Factor `Float` — How quickly density falls off
- Seed `Integer` — Random seed
- Keep Boundaries `Boolean` — Preserve the boundary of the input
- Inset `Float` — Distance to inset from the boundary

**Outputs**

- Geometry `Geometry` — Triangulated geometry


### A3D_Derivative

**Description**

Numerically differentiates a function closure at a point X using a finite-difference delta, returning the local slope and Y-intercept of the tangent line.

**Inputs**

- Function Closure `Closure` — Function to differentiate
- X `Float` — Point to evaluate the slope at
- Delta `Float` — Step size for the finite difference

**Outputs**

- Slope `Float` — Slope of the tangent line at X
- Y Intercept `Float` — Y intercept of the tangent line


### A3D_Derive Velocity

**Description**

Derives a per-point velocity vector from the difference between a previous and current position, with damping applied.

**Inputs**

- Previous Position `Vector` — Position on the previous step
- Position `Vector` — Current position
- Damping `Float` — Damping applied to the velocity

**Outputs**

- Vector `Vector` — Derived velocity


### A3D_Direction On Surface

**Description**

Projects an arbitrary direction vector onto a surface's tangent plane defined by a normal, keeping the result tangent to the surface.

**Inputs**

- Direction `Vector` — Direction to project
- Normal `Vector` — Surface normal

**Outputs**

- Vector `Vector` — Direction projected onto the surface tangent plane


### A3D_Distance From Axis

**Description**

Computes the perpendicular distance from a position to an infinite axis defined by an origin and direction.

**Inputs**

- Position `Vector` — Position to measure from
- Origin `Vector` — Point on the axis
- Axis `Vector` — Direction of the axis

**Outputs**

- Distance `Float` — Perpendicular distance from the position to the axis


### A3D_Distance From Plane

**Description**

Computes the signed distance from a position to a plane defined by an origin and two in-plane axis vectors.

**Inputs**

- Position `Vector` — Position to measure from
- Origin `Vector` — Origin of the plane
- U Axis `Vector` — First in-plane axis
- V Axis `Vector` — Second in-plane axis

**Outputs**

- Distance `Float` — Signed distance from the position to the plane


### A3D_Distance to Boundary

**Description**

Computes each element's distance to the nearest open/mesh boundary edge.

**Inputs**

- Geometry `Geometry` — Geometry to measure boundary distance on

**Outputs**

- Distance `Float` — Number of topology steps to the nearest edge


### A3D_Dodecahedron

**Description**

Generates a regular dodecahedron mesh of a given radius, built from a convex hull of instanced pentagonal faces.

**Inputs**

- Radius `Float` — Radius of the dodecahedron

**Outputs**

- Mesh `Geometry` — Generated dodecahedron mesh


### A3D_Domain Index

**Description**

Returns the index of the current element for a selectable geometry domain (point, edge, face, etc.), abstracting over Blender's per-domain index nodes.

**Inputs**

- Domain `Menu` — Domain to evaluate Index Field on

**Outputs**

- Index `Integer` — Index of the selected Domain type.


### A3D_Edge Array

**Description**

Distributes instanced or inset geometry along selected edges at a controllable spacing/count, with per-instance scale, alignment, rotation, and randomized selection.

**Inputs**

- Mesh `Geometry` — Geometry whose elements are iterated over
- Selection `Boolean` — Selection on the iteration domain
- Inset `Float` — Inset applied to the generated geometry
- Radius `Float` — The radius of the cylinder
- Depth `Float` — The height of the cylinder
- Vertices `Integer` — The number of vertices on the top and bottom circles
- Length `Float` — Length of each array element along the edge
- Probability `Float` — Chance that each element is generated
- Seed `Integer` — Random seed for the selection
- Instance `Geometry` — Geometry that is instanced on the points
- Pick Instance `Boolean` — Choose instances from the "Instance" input at each point instead of instancing the entire geometry
- Scale `Vector` — Scale of the instances
- Align `Boolean` — Align instances to the edge direction
- Rotation `Rotation` — Rotation applied to each instance

**Outputs**

- Mesh `Geometry` — Result of joining generated geometries from each iteration


### A3D_Edge Info

**Description**

Reports whether an edge is horizontal or vertical, its direction vector, and its length, for a given edge index.

**Inputs**

- Edge Index `Integer` — Index of the edge to read

**Outputs**

- Horizontal `Boolean` — True if the edge is horizontal
- Vertical `Boolean` — True if the edge is vertical
- Direction `Vector` — Direction vector of the edge
- Length `Float` — Length of the edge


### A3D_Expand Selection

**Description**

Grows or shrinks a boolean selection outward across a chosen domain by a number of steps, with probabilistic falloff and seeded randomness.

**Inputs**

- Selection `Boolean` — Selection to expand
- Steps `Integer` — Number of steps to grow the selection
- Domain `Menu` — Domain to expand across
- Mode `Menu` — Whether the selection grows or shrinks
- Probability `Float` — Chance that each neighbor is included per step
- Seed `Integer` — Random seed

**Outputs**

- Result `Boolean` — Expanded selection


### A3D_Extended Camera Info

**Description**

A comprehensive camera data node. combines transform, projection matrix, focal length, sensor size, shift, clipping planes, focus distance, orthographic state/scale, and both view distance/direction and field-of-view in one lookup.

**Inputs**

- Source `Menu` — Where the camera comes from
- Camera `Object` — Camera object to read

**Outputs**

- Transform `Matrix` — Transformation matrix containing the location, rotation and scale of the camera
- Location `Vector` — Location of the camera
- Rotation `Rotation` — Rotation of the camera
- Scale `Vector` — Scale of the camera
- Projection Matrix `Matrix` — Camera projection matrix
- Focal Length `Float` — Perspective camera focal length
- Sensor `Vector` — Size of the camera sensor
- Shift `Vector` — Camera shift
- Clip Start `Float` — Camera near clipping distance
- Clip End `Float` — Camera far clipping distance
- Focus Distance `Float` — Distance to the focus point for depth of field
- Is Orthographic `Boolean` — Whether the camera is using orthographic projection
- Orthographic Scale `Float` — Orthographic camera scale (similar to zoom)
- Distance `Float` — Distance from the camera to the evaluated position
- Direction `Vector` — Direction from the camera to the evaluated position
- Horizontal FOV `Float` — Horizontal field of view of the camera
- Vertical FOV `Float` — Vertical field of view of the camera


### A3D_Extended Vertex Neighbors

**Description**

Returns a sortable pair of neighboring vertex indices around a given vertex, along with the total connected vertex and face counts.

**Inputs**

- Vertex Index `Integer` — The vertex to retrieve data from. Defaults to the vertex from the context
- Sort Index `Integer` — Which of the sorted edges to output

**Outputs**

- Vertex Index 1 `Integer` — Index of the first sorted neighboring vertex
- Vertex Index 2 `Integer` — Index of the second sorted neighboring vertex
- Vertex Count `Integer` — The number of vertices connected to this vertex with an edge, equal to the number of connected edges
- Face Count `Integer` — Number of faces that contain the vertex


### A3D_Face Corner Info

**Description**

Returns the position and corner index of a specific corner of a given face, offset from a weighted reference corner.

**Inputs**

- Face Index `Integer` — The face to retrieve data from. Defaults to the face from the context
- Weights `Float` — Values used to sort the face's corners. Uses indices by default
- Offset `Integer` — The number of corners to move around the face before finding the result, circling around the start of the face if necessary

**Outputs**

- Position `Vector` — Position of the resulting corner
- Corner Index `Integer` — A corner of the face, chosen by the sort index


### A3D_Face Winding Direction

**Description**

Returns the signed winding direction (+1/-1) of the current face, useful for detecting flipped normals or inconsistent topology.

**Inputs**

_None — reads directly from the geometry context (e.g. current point/face/edge)._

**Outputs**

- Sign `Float` — Winding direction of the face, +1 or -1


### A3D_Fermat Spiral

**Description**

Generates a set of points arranged in a Fermat (golden-angle) spiral, controlled by point count and a scaling factor. Commonly used for even radial packing.

**Inputs**

- Count `Integer` — The number of points to create
- Scaling Factor `Float` — Scales the spread of the spiral

**Outputs**

- Points `Geometry` — Generated spiral points


### A3D_Gaussian Curvature

**Description**

Estimates per-vertex Gaussian curvature via angle defect (the deviation of the sum of incident face angles from 2π), for curvature-driven shading or deformation.

**Inputs**

_None — reads directly from the geometry context (e.g. current point/face/edge)._

**Outputs**

- Curvature `Float` — Gaussian curvature at each vertex


### A3D_Geometry Motion Path

**Description**

Builds a trailing motion-path mesh from a set of animated points, with configurable substeps and a maximum trail age.

**Inputs**

- Points `Geometry` — Animated points to trace
- Selection `Boolean` — Points to include
- Substeps `Integer` — Quality of inbetween motion estimation
- Max Trail Age `Float` — Maximum age of the trail before it is removed

**Outputs**

- Geometry `Geometry` — Generated motion path geometry


### A3D_Golden Ratio

**Description**

Outputs the constant φ (the golden ratio, ≈1.618) for use in proportion-driven procedural setups.

**Inputs**

_None — reads directly from the geometry context (e.g. current point/face/edge)._

**Outputs**

- φ `Float` — The golden ratio, approximately 1.618


### A3D_Grid Float Neighbors 2D

**Description**

Samples a 3×3 neighborhood of float values around a given index in a resolution-addressed grid, returning each row of neighboring values.

**Inputs**

- Resolution `Integer` — Number of vertices in the X direction
- Value `Float` — Float value to sample the neighbors of
- Index `Integer` — Index of the center cell

**Outputs**

- Row 1 `Float` — Neighbor at row 1 of column 1
- Row 2 `Float` — Neighbor at row 2 of column 1
- Row 3 `Float` — Neighbor at row 3 of column 1
- Row 1 `Float` — Neighbor at row 1 of column 2
- Row 3 `Float` — Neighbor at row 3 of column 2
- Row 1 `Float` — Neighbor at row 1 of column 3
- Row 2 `Float` — Neighbor at row 2 of column 3
- Row 3 `Float` — Neighbor at row 3 of column 3


### A3D_Grid Integer Neighbors 2D

**Description**

Samples a 3×3 neighborhood of integer values around a given index in a resolution-addressed grid, returning each row of neighboring values.

**Inputs**

- Resolution `Integer` — Number of vertices in the X direction
- Value `Integer` — Integer value to sample the neighbors of
- Index `Integer` — Index of the center cell

**Outputs**

- Row 1 `Integer` — Neighbor at row 1 of column 1
- Row 2 `Integer` — Neighbor at row 2 of column 1
- Row 3 `Integer` — Neighbor at row 3 of column 1
- Row 1 `Integer` — Neighbor at row 1 of column 2
- Row 3 `Integer` — Neighbor at row 3 of column 2
- Row 1 `Integer` — Neighbor at row 1 of column 3
- Row 2 `Integer` — Neighbor at row 2 of column 3
- Row 3 `Integer` — Neighbor at row 3 of column 3


### A3D_Grid Laplacian 2D

**Description**

Computes a discrete Laplacian (second-difference) of a value field across grid-connected edges, up to a maximum edge count.

**Inputs**

- Value `Float` — Value field to take the Laplacian of
- Max Edges `Integer`

**Outputs**

- Value `Float` — Laplacian of the value field


### A3D_Grid Selection Kernel 2D

**Description**

Builds a boolean selection over a rectangular width/height kernel positioned at an index within a resolution-addressed grid.

**Inputs**

- Index `Integer` — Index of the grid cell the kernel is positioned at
- Height `Integer` — Height of the kernel in cells
- Width `Integer` — Width of the kernel in cells
- Resolution `Integer` — Resolution of the grid

**Outputs**

- Boolean `Boolean` — True for cells inside the kernel


### A3D_Grid Vector Neighbors 2D

**Description**

Samples a 3×3 neighborhood of vector values around a given index in a resolution-addressed grid, returning each row of neighboring values.

**Inputs**

- Resolution `Integer` — Number of vertices in the X direction
- Value `Vector` — Vector value to sample the neighbors of
- Index `Integer` — Index of the center cell

**Outputs**

- Row 1 `Vector` — Neighbor at row 1 of column 1
- Row 2 `Vector` — Neighbor at row 2 of column 1
- Row 3 `Vector` — Neighbor at row 3 of column 1
- Row 1 `Vector` — Neighbor at row 1 of column 2
- Row 3 `Vector` — Neighbor at row 3 of column 2
- Row 1 `Vector` — Neighbor at row 1 of column 3
- Row 2 `Vector` — Neighbor at row 2 of column 3
- Row 3 `Vector` — Neighbor at row 3 of column 3


### A3D_Ground Impact Solve

**Description**

Analytically solves for where and when a ballistic trajectory (defined by an initial position, velocity, and gravity) intersects a plane, returning the impact time, position, and velocity.

**Inputs**

- Initial Position `Vector` — Position at launch
- Initial Velocity `Vector` — Velocity at launch
- Gravity `Vector` — Gravity acceleration vector
- Plane Point `Vector` — Point on the plane
- Plane Normal `Vector` — Normal of the plane

**Outputs**

- Impact Time `Float` — Time until the trajectory reaches the plane
- Impact Position `Vector` — Position where the trajectory reaches the plane
- Impact Velocity `Vector` — Velocity at the moment of impact


### A3D_Grow on Surface

**Description**

Grows a path of points across a surface from a starting direction, stepping and rotating with each iteration and staying offset from the surface .

**Inputs**

- Points `Geometry` — Starting points of the paths
- Geometry `Geometry` — Surface to grow across
- Start Direction `Vector` — Initial direction of the particles
- Rotation Angle `Float` — How much the particle can turn each step
- Step Size `Float` — Distance particle travels in one frame
- Surface Offset `Float` — Offset to keep particle from clipping through surface

**Outputs**

- Geometry `Geometry` — Grown path geometry


### A3D_Harmonic Field

**Description**

Propagates a starting scalar value across a mesh from source points toward sink points over a number of iterations, returning both the updated mesh and its gradient field.

**Inputs**

- Mesh `Geometry` — Mesh to propagate the value across
- Starting Value `Float` — Value assigned at the sources
- Iterations `Integer` — Number of propagation iterations
- Sinks `Boolean` — Points the value flows toward
- Sources `Boolean` — Points the value flows from

**Outputs**

- Mesh `Geometry` — Mesh with the propagated value
- Gradient `Float` — Gradient of the propagated field


### A3D_Helix

**Description**

Displaces curve points into a helical pattern around the curve's path, driven by frequency, amplitude, and phase.

**Inputs**

- Curves `Geometry` — Curves to displace
- Source `Menu` — Source used to orient the helix
- Frequency `Float` — Tightness of the spiral
- Amplitude `Float` — Radius of the spiral
- Phase `Float` — Offset of the spiral

**Outputs**

- Curves `Geometry` — Curves displaced into a helix


### A3D_IK Solver

**Description**

Solves inverse kinematics for a chain of geometry between a start and end point (with an optional pole target), iterating to convergence.

**Inputs**

- Geometry `Geometry` — Chain to solve
- Iterations `Integer` — Number of solver iterations
- Start `Vector` — Position of the chain root
- End `Vector` — Target position for the end of the chain
- Pole `Vector` — Pole target controlling the bend direction

**Outputs**

- Geometry `Geometry` — Solved chain


### A3D_Index of Grid Coordinate

**Description**

Converts 2D (X, Y) grid coordinates into a flat index for a grid of a given resolution, with an in-bounds check.

**Inputs**

- Resolution `Integer` — Resolution of the grid
- X `Integer` — X coordinate in the grid
- Y `Integer` — Y coordinate in the grid

**Outputs**

- Index `Integer` — Flat index of the coordinate
- In Bounds `Boolean` — True if the coordinate is inside the grid


### A3D_Inset Faces

**Description**

Face inset operation supporting individual or grouped insets, independent thickness/depth control, and even-distance/even-depth modes, returning the inset mesh split into inner and outer face groups.

**Inputs**

- Mesh `Geometry` — Mesh to inset faces on
- Selection `Boolean` — Faces to inset
- Individual `Boolean` — Inset each face separately
- Thickness `Float` — Amount to inset by
- Depth `Float` — Offset of the inset faces along their normal
- Even Distance `Boolean` — Keep the inset distance even around corners
- Even Depth `Boolean` — Keep the depth even across angled faces

**Outputs**

- Mesh `Geometry` — Mesh with the faces inset
- Inner `Boolean` — Faces created by the inset
- Outer `Boolean` — Faces surrounding the inset faces


### A3D_Inside BBox

**Description**

Tests whether a position lies inside the bounding box of the input geometry.

**Inputs**

- Geometry `Geometry` — Geometry whose bounding box is tested
- Position `Vector` — Position to test

**Outputs**

- Inside `Boolean` — True if the position is inside the bounding box


### A3D_Inside Frustum

**Description**

Tests whether a position lies inside a camera's view frustum, with configurable padding.

**Inputs**

- Source `Menu` — Where the camera comes from
- Camera `Object` — Camera object whose frustum is tested
- Position `Vector` — Position to sample (Default Position)
- Horizontal Padding `Float` — Amount to extend the frustum horizontally, along the camera's X axis
- Vertical Padding `Float` — Amount to extend the frustum vertically, along the camera's Y axis

**Outputs**

- In Frustum `Boolean` — Returns true if the position is inside the frustum


### A3D_Inside Frustum (Legacy)

**Description**

An earlier frustum-containment test driven by explicit render resolution, padding, and camera FOV rather than direct camera data.

**Inputs**

- Use Active Camera `Boolean` — Use the active scene camera
- Culling Camera `Object` — Camera object to test against
- Horizontal Resolution `Integer` — Horizontal render resolution
- Vertical Resolution `Integer` — Vertical render resolution
- Horizontal Padding `Float` — Amount to extend the frustum horizontally
- Vertical Padding `Float` — Amount to extend the frustum vertically
- Camera FOV `Float` — Field of view of the camera
- Position `Vector` — Position to test

**Outputs**

- Inside Frustum `Boolean` — True if the position is inside the frustum


### A3D_Inside Prism

**Description**

Tests whether a position lies inside a prism volume defined by four reference points.

**Inputs**

- Position `Vector` — Position to test
- A `Vector` — First reference point of the prism
- B `Vector` — Second reference point of the prism
- C `Vector` — Third reference point of the prism
- D `Vector` — Fourth reference point of the prism

**Outputs**

- Boolean `Boolean` — True if the position is inside the prism


### A3D_Inside Quad Face

**Description**

Tests whether a position lies inside the bounds of a specific quad face.

**Inputs**

- Position `Vector` — Position to test
- Face Index `Integer` — Index of the quad face

**Outputs**

- Inside `Boolean` — True if the position is inside the face


### A3D_Inside Rectangle

**Description**

Tests whether a position lies inside a rectangle defined by three of its corner vertices.

**Inputs**

- Position `Vector` — Position to test
- Vertex A `Vector` — First corner of the rectangle
- Vertex B `Vector` — Second corner of the rectangle
- Vertex C `Vector` — Third corner of the rectangle

**Outputs**

- Boolean `Boolean` — True if the position is inside the rectangle


### A3D_Instance Info

**Description**

Returns the bounding min, max, and origin of the current instance.

**Inputs**

_None — reads directly from the geometry context (e.g. current point/face/edge)._

**Outputs**

- Min `Vector` — Minimum corner of the instance bounds
- Max `Vector` — Maximum corner of the instance bounds
- Origin `Vector` — Origin of the instance


### A3D_Instance Info (Legacy)

**Description**

An earlier version of Instance Info that takes an explicit instances input rather than reading the current instance context.

**Inputs**

- Instances `Geometry` — Instances to read the bounds from

**Outputs**

- Min `Vector` — Minimum corner of the instance bounds
- Max `Vector` — Maximum corner of the instance bounds
- Origin `Vector` — Origin of the instance


### A3D_Instance Matrix

**Description**

Builds an instance transform matrix from a mesh and instance geometry, with depth, selection, and instance-index/pick-instance controls.

**Inputs**

- Mesh `Geometry` — Mesh the instances are placed on
- Instance `Geometry` — Geometry to instance
- Depth `Float` — Depth of the instances
- Selection `Boolean` — Elements to place instances on
- Instance Index `Integer` — Index of the instance used for each point. This is only used when Pick Instances is on. By default the point index is used
- Pick Instance `Boolean` — Choose instances from the "Instance" input at each point instead of instancing the entire geometry

**Outputs**

- Instances `Geometry` — Generated instances


### A3D_Instance on Faces

**Description**

Instances geometry onto selected faces of a mesh, with pick-instance and instance-index controls for choosing which instance goes where.

**Inputs**

- Mesh `Geometry` — Mesh whose faces receive instances
- Selection `Boolean` — Faces to place instances on
- Instance `Geometry` — Geometry that is instanced on the faces
- Pick Instance `Boolean` — Choose instances from the "Instance" input at each face instead of instancing the entire geometry
- Instance Index `Integer` — Index of the instance used for each face. This is only used when Pick Instance is on. By default the face index is used

**Outputs**

- Instances `Geometry` — Generated instances


### A3D_Integer Clamp

**Description**

Clamps an integer value between a minimum and maximum.

**Inputs**

- Value `Integer` — Value to clamp
- Min `Integer` — Minimum allowed value
- Max `Integer` — Maximum allowed value

**Outputs**

- Value `Integer` — Clamped value


### A3D_Laplacian

**Description**

A generalized Laplacian (connectivity-based blur) operator that works across float, integer, and vector value types over a given number of iterations.

**Inputs**

- Value `Float` — Float value to blur
- Integer `Integer` — Integer value to blur
- Vector `Vector` — Vector value to blur
- Iterations `Integer` — How many times to blur the values for all elements

**Outputs**

- Value `Float` — Blurred float value
- Integer `Integer` — Blurred integer value
- Vector `Vector` — Blurred vector value


### A3D_Largest Island

**Description**

Returns a boolean selection marking the largest connected mesh island.

**Inputs**

_None — reads directly from the geometry context (e.g. current point/face/edge)._

**Outputs**

- Boolean `Boolean` — Is the largest mesh island


### A3D_Line Intersect

**Description**

Tests whether two line segments (each defined by two endpoints) intersect.

**Inputs**

- Edge A Position 1 `Vector` — First endpoint of edge A
- Edge A Position 2 `Vector` — Second endpoint of edge A
- Edge B Position 1 `Vector` — First endpoint of edge B
- Edge B Position 2 `Vector` — Second endpoint of edge B

**Outputs**

- Intersect `Boolean` — True if the two segments intersect


### A3D_Line Intersect Point

**Description**

Computes the intersection point of two line segments (each defined by two endpoints), assuming they intersect.

**Inputs**

- Edge A Position 1 `Vector` — First endpoint of edge A
- Edge A Position 2 `Vector` — Second endpoint of edge A
- Edge B Position 1 `Vector` — First endpoint of edge B
- Edge B Position 2 `Vector` — Second endpoint of edge B

**Outputs**

- Intersection Point `Vector` — Point where the two segments intersect


### A3D_Line-Line Intersection

**Description**

Combines intersection testing and position calculation for two line segments into a single node, returning both whether they intersect and where.

**Inputs**

- Edge A Position 1 `Vector` — First endpoint of edge A
- Edge A Position 2 `Vector` — Second endpoint of edge A
- Edge B Position 1 `Vector` — First endpoint of edge B
- Edge B Position 2 `Vector` — Second endpoint of edge B

**Outputs**

- Intersects `Boolean` — True if the two segments intersect
- Intersection Position `Vector` — Point where the two segments intersect


### A3D_Looping Coordinates

**Description**

Generates cyclically looping XYZ and W coordinates over a given loop duration, for seamless periodic animation or tiling.

**Inputs**

- Loop Duration `Integer` — Number of frames in one loop

**Outputs**

- XYZ `Vector` — Looping XYZ coordinates
- W `Float` — Looping W coordinate


### A3D_Make Curve Acyclic

**Description**

Converts a cyclic (closed) curve into an acyclic (open) curve while preserving its shape.

**Inputs**

- Curve `Geometry` — Curve to open

**Outputs**

- Curve `Geometry` — Curve with cyclic splines made acyclic


### A3D_Merge by Distance

**Description**

Merges mesh elements within a given distance of each other, with options to limit merging to islands and to merge by group ID.

**Inputs**

- Mesh `Geometry` — Point cloud or mesh to merge points of
- Limit Islands `Boolean` — Only merge elements within the same island
- Group ID `Integer` — Only merge elements with the same group ID
- Position `Vector` — Position used to measure distances
- Distance `Float` — Maximum distance between elements to merge

**Outputs**

- Mesh `Geometry` — Mesh with nearby elements merged


### A3D_Mesh to Lattice

**Description**

Converts a mesh into a lattice-cell structure using a selectable cell type and object, with a configurable cell size and interior band width.

**Inputs**

- Mesh `Geometry` — Mesh to convert
- Cell Type `Menu` — Type of cell to use for each lattice element
- Cell Object `Object` — Object used as the lattice cell, must be exactly 1m³
- Cell Size `Float` — Size of each lattice cell
- Interior Band Width `Float` — Width of the gradient inside of the mesh

**Outputs**

- Mesh `Geometry` — Lattice generated from the mesh


### A3D_Midpoint Range to Min Max

**Description**

An alternate/duplicate implementation of Midpoint Range, converting a midpoint-and-range pair into explicit min/max bounds.

**Inputs**

- Midpoint `Float` — Center of the range
- Range `Float` — Total width of the range

**Outputs**

- Min `Float` — Lower bound of the range
- Max `Float` — Upper bound of the range


### A3D_Mirror

**Description**

Mirrors a mesh across chosen X/Y/Z axes, either about the origin or about a separate mirror object.

**Inputs**

- Mesh `Geometry` — Mesh to mirror
- X `Boolean` — Mirror across the X axis
- Y `Boolean` — Mirror across the Y axis
- Z `Boolean` — Mirror across the Z axis
- Use Object `Boolean` — Mirror about an object instead of the origin
- Mirror Object `Object` — Object to mirror about

**Outputs**

- Mesh `Geometry` — Mirrored mesh


### A3D_Multivariate Newton Solver

**Description**

Solves a system of equations for a root using multivariate Newton's method, iterating from an initial guess with a configurable step size and function closure.

**Inputs**

- Function Closure `Closure` — Function to find the root of
- Iterations `Integer` — Number of Newton iterations
- Initial Guess `Vector` — Starting point for the search
- Step Size `Float` — Step size used for the numerical derivative

**Outputs**

- Root `Vector` — Root found by the solver


### A3D_N Nearest Neighbors

**Description**

Finds the N nearest neighboring points to each input point.

**Inputs**

- Points `Geometry` — Points to find neighbors for
- Neighbors `Integer` — Number of nearest neighbors to find

**Outputs**

- Points `Geometry` — Points with neighbor connections


### A3D_Nearest Point Info

**Description**

Returns the index, radius, distance, direction, and offset of the nearest point (optionally within a group ID) to a given position.

**Inputs**

- Position `Vector` — Position to sample from
- Group ID `Integer` — Splits the geometry into groups which can be sampled individually

**Outputs**

- Index `Integer` — Index of Nearest
- Radius `Float` — 'radius' attribute of Nearest
- Distance `Float` — Distance to Nearest
- Direction `Vector` — Normalized direction towards Nearest
- Offset `Vector` — Offset between current and Nearest


### A3D_Neighbors of Vertex

**Description**

Returns a weighted, sortable list of a vertex's connected neighbor vertices and their total count.

**Inputs**

- Vertex Index `Integer` — The vertex to retrieve data from. Defaults to the vertex from the context
- Weights `Float` — Values used to sort the edges connected to the vertex. Uses indices by default
- Sort Index `Integer` — Which of the sorted edges to output. Negative indexing is supported

**Outputs**

- Other Vertex `Integer` — Index of the selected neighboring vertex
- Total `Integer` — Number of vertices connected to this vertex


### A3D_Node Name

**Description**

One or two sentences on what the node does and what it returns.

**Inputs**

- Socket Name `Type` — Short description of the socket
- Another Socket `Type` — Short description

**Outputs**

- Socket Name `Type` — Short description


### A3D_Noodle

**Description**

Generates a tube ('noodle') mesh along a curve, with adjustable scale and profile/cap resolution.

**Inputs**

- Curve `Geometry` — Curve to generate the tube along
- Scale `Float` — Radius of the tube
- Profile Resolution `Integer` — Number of points around the tube profile
- Cap Resolution `Integer` — Number of segments in each end cap

**Outputs**

- Mesh `Geometry` — Generated tube mesh


### A3D_Normalize Field

**Description**

Remaps a per-element float attribute to the 0–1 range based on the minimum and maximum values found across the field's domain.

**Inputs**

- Value `Float` — The values the minimum and maximum will be calculated from
- Group ID `Integer` — An index used to group values together for multiple separate operations

**Outputs**

- Normalized Value `Float` — Value remapped to the 0-1 range


### A3D_Object Motion Path

**Description**

Builds a trailing motion-path mesh tracking an object's movement over time, with configurable substeps and maximum trail age.

**Inputs**

- Object `Object` — Object to trace
- Substeps `Integer` — Quality of inbetween motion estimation
- Max Trail Age `Float` — Maximum age of the trail before it is removed

**Outputs**

- Geometry `Geometry` — Generated motion path geometry


### A3D_Octree

**Description**

Builds an octree spatial subdivision of a point cloud between a min and max bound, iterating to the target depth.

**Inputs**

- Points `Geometry` — Points to subdivide
- Iterations `Integer` — Number of subdivision levels
- Min `Vector` — Minimum corner of the bounds
- Max `Vector` — Maximum corner of the bounds

**Outputs**

- Geometry `Geometry` — Generated octree geometry


### A3D_Opposite Corner of Triangle Adjacent to Edge

**Description**

Returns the vertex opposite an edge in a triangle attached to that edge, with weights and a sort index to choose between the attached corners.

**Inputs**

- Edge Index `Integer` — The edge to retrieve data from. Defaults to the edge from the context
- Weights `Float` — Values that sort the corners attached to the edge
- Sort Index `Integer` — Which of the sorted corners to output. Negative indexing is supported

**Outputs**

- Vertex Index `Integer` — The vertex the corner is attached to


### A3D_Pack Curves

**Description**

Packs curve geometry onto a target panel/surface using a cost-based path-growth algorithm (base cost plus per-step increment), respecting a vertex group and a maximum curve count.

**Inputs**

- Geometry `Geometry` — Geometry to pack curves onto
- Selection `Boolean` — Parts of the geometry to pack curves onto
- Base Path Cost `Float` — Starting cost of each path
- Path Cost Increment `Float` — Cost added per step along a path
- Vertex Group `String` — Name of the vertex group that limits the packing
- Max Curves `Integer` — Maximum number of curves to generate
- Seed `Integer` — Random seed
- Panel `Boolean` — Restrict packing to the target panel
- Target Position `Vector` — Position the curves are packed toward

**Outputs**

- Curve `Geometry` — Packed curves


### A3D_Particle Tracking

**Description**

Emits and tracks particles toward a target position with per-particle emission/tracking delay and velocity ranges plus noise-driven trajectory variation, outputting velocity and age attributes.

**Inputs**

- Geometry `Geometry` — Geometry to emit particles from
- Selection `Boolean` — Points that emit particles
- Target Position `Vector` — (Required) world space point particles tend to follow
- Emission Delay Min `Float` — Minimum time to wait before emitting a particle
- Emission Delay Max `Float` — Maximum time to wait before emitting a particle
- Emission Velocity `Float` — Initial velocity during the launch phase, before Tracking Delay has elapsed
- Tracking Delay `Float` — Time to wait before the particle begins to seek Target Position
- Tracking Velocity `Float` — Velocity during the tracking phase, after Tracking Delay has elapsed
- Trajectory Noise Scale `Float` — Scale of noise that alters trajectory
- Trajectory Noise Strength `Float` — Strength of noise that alters trajectory

**Outputs**

- Geometry `Geometry` — Emitted particles
- Velocity `Vector` — Velocity of each particle
- Age `Float` — Current age of each particle
- Start Age `Float` — Age at which each particle starts


### A3D_Patch Mesh

**Description**

Fills or patches holes in a mesh's topology.

**Inputs**

- Mesh `Geometry` — Mesh to patch

**Outputs**

- Mesh `Geometry` — Mesh with holes filled


### A3D_PBD Solver Repeat

**Description**

Runs a position-based dynamics (PBD) solve over multiple outer iterations and substeps, with fixed points, external force, damping, stretch stiffness, pretension, volume preservation, and mesh collision.

**Inputs**

- Geometry `Geometry` — Rope geometry to simulate
- Iterations `Integer` — Number of constraint solver iterations
- Substeps `Integer` — Quality of simulation
- Fixed Points `Boolean` — Which points are fixed/immobile
- Animated `Boolean` — Are fixed points animated/updating every frame (use for rigs)
- External Force `Vector` — External force acting on simulation
- Damping `Float` — Velocity reduction (recommended >0)
- Stretch Stiffness `Float` — How much the rope resists stretching. High values require higher steps
- Pretension `Float` — Tension in the rope before simulation. Helps keep ropes stiff
- Preserve Volume `Boolean` — Keep the rope from losing volume when stretched
- Collision `Boolean` — Enable collision with a mesh
- Collision Mesh `Geometry` — Mesh the rope collides with

**Outputs**

- Geometry `Geometry` — Simulated rope geometry


### A3D_Plane Normal

**Description**

Computes the normal vector of the plane defined by three points.

**Inputs**

- Point A `Vector` — First point on the plane
- Point B `Vector` — Second point on the plane
- Point C `Vector` — Third point on the plane

**Outputs**

- Vector `Vector` — Normal vector of the plane


### A3D_Plexus

**Description**

Builds a connective 'plexus' mesh linking nearby points based on a connectivity parameter, commonly used for network/energy-field visuals.

**Inputs**

- Points `Geometry` — Points to connect
- Connectivity `Integer` — Maximum number of connections per point

**Outputs**

- Mesh `Geometry` — Generated network of connections


### A3D_Point Slope Line

**Description**

Constructs a line segment of a given length from a point-slope definition (X, Y, slope), returning its start and end points.

**Inputs**

- X `Float` — X coordinate of the point
- Y `Float` — Y coordinate of the point
- Slope `Float` — Slope of the line
- Length `Float` — Length of the line segment

**Outputs**

- Start Point `Vector` — Start of the line segment
- End Point `Vector` — End of the line segment


### A3D_Poke Faces

**Description**

Pokes (fan-triangulates from a center point) all faces in the input geometry.

**Inputs**

- Geometry `Geometry` — Geometry to poke faces on

**Outputs**

- Geometry `Geometry` — Geometry with faces poked


### A3D_Poke Triangle

**Description**

Pokes a single face at a given position, splitting it into a triangle fan from that point.

**Inputs**

- Mesh `Geometry` — Mesh containing the face to poke
- Position `Vector` — Location of central vertex

**Outputs**

- Mesh `Geometry` — Mesh with the face poked


### A3D_Position Components

**Description**

Splits the current position attribute into its X, Y, and Z components.

**Inputs**

_None — reads directly from the geometry context (e.g. current point/face/edge)._

**Outputs**

- X `Float` — X component of the position
- Y `Float` — Y component of the position
- Z `Float` — Z component of the position


### A3D_Project To Plane

**Description**

Projects a position onto a plane defined by an origin and normal.

**Inputs**

- Position `Vector` — Position to project
- Origin `Vector` — Origin of the plane
- Plane Normal `Vector` — Normal of the plane

**Outputs**

- Vector `Vector` — Position projected onto the plane


### A3D_Quad Corners

**Description**

Returns the four corner positions (A–D) of a quad face at a given offset.

**Inputs**

- Face Index `Integer` — The face to retrieve data from. Defaults to the face from the context
- Offset `Integer` — Number of corners to rotate the corner order by

**Outputs**

- Corner A `Vector` — Position of the first corner
- Corner B `Vector` — Position of the second corner
- Corner C `Vector` — Position of the third corner
- Corner D `Vector` — Position of the fourth corner


### A3D_Quad Sphere

**Description**

Generates a quad-topology sphere (cube-projected) of a given radius and subdivision level, with a UV map output.

**Inputs**

- Radius `Float` — Radius of the sphere
- Subdivisions `Integer` — Number of subdivisions per cube face

**Outputs**

- Mesh `Geometry` — Generated sphere mesh
- UV Map `Vector` — UV coordinates of the sphere


### A3D_Quad Tangent

**Description**

Computes the tangent vector of a quad face.

**Inputs**

- Face Index `Integer` — The face to retrieve data from. Defaults to the face from the context

**Outputs**

- Tangent `Vector` — Vector pointing along the longest axis of the face


### A3D_Random Point In Shell

**Description**

Generates a seeded random point within a spherical shell between a minimum and maximum radius.

**Inputs**

- Min Radius `Float` — Radius of inner boundary
- Max Radius `Float` — Radius of outer boundary
- ID `Integer` — ID used to vary the random value per element
- Seed `Integer` — Random Seed

**Outputs**

- Position `Vector` — Random position within the shell


### A3D_Random Triangulate

**Description**

Randomly triangulates a subset of the mesh's faces based on a seeded probability.

**Inputs**

- Mesh `Geometry` — Mesh to triangulate
- Probability `Float` — Chance that each face is triangulated
- Seed `Integer` — Random seed

**Outputs**

- Mesh `Geometry` — Mesh with some faces triangulated


### A3D_Random XY+Z

**Description**

Generates a seeded random vector with independently ranged XY (planar) and Z (vertical) components.

**Inputs**

- XY Min `Float` — Minimum of the X and Y components
- XY Max `Float` — Maximum of the X and Y components
- Z Min `Float` — Minimum of the Z component
- Z Max `Float` — Maximum of the Z component
- ID `Integer` — ID used to vary the random value per element
- Seed `Integer` — Random seed

**Outputs**

- Vector `Vector` — Random vector


### A3D_Roll Curve

**Description**

Rolls (twists) a curve's cross-section around its tangent by a factor and tightness, with a custom roll vector and free/flip controls.

**Inputs**

- Curve `Geometry` — Curve to roll
- Factor `Float` — Amount of roll applied
- Tightness `Float` — How tightly the roll follows the curve
- Roll Vector `Menu` — How the vector to roll about is chosen
- Free `Vector` — Roll direction used when the roll vector is free
- Flip `Boolean` — Flip the roll direction

**Outputs**

- Curve `Geometry` — Rolled curve


### A3D_Scatter Points

**Description**

Scatters points across a mesh surface using a selectable distribution mode, minimum spacing, and density falloff, returning per-point normal and rotation. When 'Use Rest Position' is True and the 'rest_position' attribute exists on the Geometry, the point positions are transferred from the un-deformed mesh to avoid popping.

**Inputs**

- Mesh `Geometry` — Mesh to scatter points on
- Mode `Menu` — Change distribution mode
- Selection `Boolean` — Faces to scatter points on
- Distance Min `Float` — Minimum spacing between points
- Density `Float` — Number of points per unit area
- Density Factor `Float` — Factor to scale the density by
- Seed `Integer` — Random seed
- Radius `Float` — Radius stored on each point
- Use Rest Position `Boolean` — Requires enabling 'Rest Position' in the Shape Keys panel

**Outputs**

- Points `Geometry` — Scattered points
- Normal `Vector` — Surface normal at each point
- Rotation `Rotation` — Rotation aligned to the surface at each point


### A3D_Seam Distance

**Description**

Computes each point's distance to the nearest UV seam.

**Inputs**

- Mesh `Geometry` — Mesh to measure the seam distance on
- UVMap `String` — Name of the UV map to read seams from
- Seam Attribute `String` — Name of the attribute marking seam edges

**Outputs**

- Mesh `Geometry` — Mesh after the seam distance calculation
- Distance `Float` — Distance to the nearest UV seam


### A3D_Set Position by Attribute

**Description**

Sets a mesh's point positions directly from a named vector attribute.

**Inputs**

- Mesh `Geometry` — Mesh whose point positions are replaced
- Attribute `String` — Name of the vector attribute to use as positions

**Outputs**

- Geometry `Geometry` — Geometry with positions set from the attribute


### A3D_Smooth Curve

**Description**

Smooths a curve's control points over a number of iterations, with a selectable mode and target segment count/length.

**Inputs**

- Curve `Geometry` — Curve to smooth
- Iterations `Integer` — Number of smoothing iterations
- Mode `Menu` — How to specify the amount of samples
- Count `Integer` — Number of segments to resample to
- Length `Float` — Segment length to resample to

**Outputs**

- Curve `Geometry` — Smoothed curve


### A3D_Solve XPBD Edge Constraints

**Description**

Solves extended position-based dynamics (XPBD) edge/distance constraints for a given stiffness and tension over a maximum iteration count, returning the accumulated position correction.

**Inputs**

- Max Iterations `Integer` — Maximum number of solver iterations
- Stiffness `Float` — Stiffness of the edge constraints
- Tension `Float` — Tension in the edges

**Outputs**

- Accumulated Correction `Vector` — Sum of the correction vectors for the point


### A3D_Sphere Collision

**Description**

Tests two indexed spheres for collision, returning whether they collided, their overlap amount, and the collision normal.

**Inputs**

- Index A `Integer` — Index of the first sphere
- Index B `Integer` — Index of the second sphere

**Outputs**

- Collided `Boolean` — True if the spheres collide
- Overlap `Float` — Amount the spheres overlap
- Normal `Vector` — Collision normal


### A3D_Split Quad

**Description**

Splits a quad face into triangles or sub-quads along a chosen direction, by a blend factor.

**Inputs**

- Mesh `Geometry` — Mesh containing the quads to split
- Factor `Float` — How far along to split the face. 0.5 is the middle of the face
- Direction `Menu` — Relative direction to split the face

**Outputs**

- Mesh `Geometry` — Mesh with the quads split


### A3D_Split to Instances

**Description**

Splits geometry into separate instances by a chosen domain and group ID, with a selectable pivot point.

**Inputs**

- Pivot Point `Menu` — Pivot point of each instance
- Domain `Menu` — Domain to split
- Geometry `Geometry` — Geometry to split into instances
- Selection `Boolean` — Elements to include
- Group ID `Integer` — Elements with the same ID go into the same instance

**Outputs**

- Instances `Geometry` — Generated instances
- Group ID `Integer` — Group ID of each instance


### A3D_Split to Instances_Edge

**Description**

Domain-locked variant of A3D_Split to Instances that splits geometry into separate instances per edge, with a pivot point type and group ID.

**Inputs**

- Pivot Point Type `Integer` — Type of pivot point of each instance
- Geometry `Geometry` — Geometry to split into instances
- Selection `Boolean` — Elements to include
- Group ID `Integer` — Elements with the same ID go into the same instance

**Outputs**

- Instances `Geometry` — Generated instances
- Group ID `Integer` — Group ID of each instance


### A3D_Split to Instances_Face

**Description**

Domain-locked variant of A3D_Split to Instances that splits geometry into separate instances per face, with a pivot point type and group ID.

**Inputs**

- Pivot Point Type `Integer` — Type of pivot point of each instance
- Geometry `Geometry` — Geometry to split into instances
- Selection `Boolean` — Elements to include
- Group ID `Integer` — Elements with the same ID go into the same instance

**Outputs**

- Instances `Geometry` — Generated instances
- Group ID `Integer` — Group ID of each instance


### A3D_Split to Instances_Instance

**Description**

Domain-locked variant of A3D_Split to Instances that splits geometry into separate instances per existing instance, with a pivot point type and group ID.

**Inputs**

- Pivot Point Type `Integer` — Type of pivot point of each instance
- Geometry `Geometry` — Geometry to split into instances
- Selection `Boolean` — Elements to include
- Group ID `Integer` — Elements with the same ID go into the same instance

**Outputs**

- Instances `Geometry` — Generated instances
- Group ID `Integer` — Group ID of each instance


### A3D_Split to Instances_Point

**Description**

Domain-locked variant of A3D_Split to Instances that splits geometry into separate instances per point, with a pivot point type and group ID.

**Inputs**

- Pivot Point Type `Integer` — Type of pivot point of each instance
- Geometry `Geometry` — Geometry to split into instances
- Selection `Boolean` — Elements to include
- Group ID `Integer` — Elements with the same ID go into the same instance

**Outputs**

- Instances `Geometry` — Generated instances
- Group ID `Integer` — Group ID of each instance


### A3D_Split to Instances_Spline

**Description**

Domain-locked variant of A3D_Split to Instances that splits geometry into separate instances per spline, with a pivot point type and group ID.

**Inputs**

- Pivot Point Type `Integer` — Type of pivot point of each instance
- Geometry `Geometry` — Geometry to split into instances
- Selection `Boolean` — Elements to include
- Group ID `Integer` — Elements with the same ID go into the same instance

**Outputs**

- Instances `Geometry` — Generated instances
- Group ID `Integer` — Group ID of each instance


### A3D_Surface Gradient

**Description**

Derives a tangential flow direction vector across a surface from an input scalar value field.

**Inputs**

- Value `Float` — Scalar field to take the gradient of

**Outputs**

- Vector `Vector` — Tangential flow direction across the surface


### A3D_Surface Normal

**Description**

Samples the surface normal of a mesh at a given position (optionally scoped by group ID), with a validity flag for out-of-bounds samples.

**Inputs**

- Mesh `Geometry` — Mesh to sample
- Group ID `Integer` — Splits the faces of the input mesh into groups which can be sampled individually
- Sample Position `Vector` — Position to sample the normal at
- Sample Group ID `Integer` — Group to sample from

**Outputs**

- Normal `Vector` — Surface normal at the sample position
- Is Valid `Boolean` — Whether the sampling was successful. It can fail when the sampled group is empty


### A3D_Sweep Curve

**Description**

Sweeps a start and end profile curve along a path curve at a given resolution, producing a lofted mesh.

**Inputs**

- Curve `Geometry` — Path curve to sweep along
- Sweep Resolution `Integer` — Number of samples along the path
- Start Profile `Geometry` — Profile curve at the start of the path
- End Profile `Geometry` — Profile curve at the end of the path
- Profile Resolution `Integer` — Number of points on the profile

**Outputs**

- Mesh `Geometry` — Swept mesh


### A3D_Tetrahedron

**Description**

Generates a regular tetrahedron mesh of a given radius.

**Inputs**

- Radius `Float` — Radius of the tetrahedron

**Outputs**

- Mesh `Geometry` — Generated tetrahedron mesh


### A3D_Tetrahedron Volume

**Description**

Computes the signed volume of a tetrahedron defined by four vertices.

**Inputs**

- Vertex A `Vector` — First vertex of the tetrahedron
- Vertex B `Vector` — Second vertex of the tetrahedron
- Vertex C `Vector` — Third vertex of the tetrahedron
- Vertex D `Vector` — Fourth vertex of the tetrahedron

**Outputs**

- Volume `Float` — Signed volume of the tetrahedron


### A3D_Univariate Newton Solver

**Description**

Solves for a root of a single-variable function closure using Newton's method, iterating from an initial guess with a configurable epsilon and step size, and reporting convergence.

**Inputs**

- Function Closure `Closure` — Function to find the root of
- Iterations `Integer` — Number of Newton iterations
- Initial Guess `Float` — Starting value for the search
- Epsilon `Float` — Tolerance used to test convergence
- Step Size `Float` — Scale of each Newton step

**Outputs**

- Root `Float` — Root found by the solver
- Converged `Boolean` — True if the solver converged


### A3D_UV Mapped Strip

**Description**

Generates a UV-mapped ribbon/strip mesh along a curve using a profile curve, with scale, tilt, UV method, channel-swap, camera-facing, and cap-fill controls.

**Inputs**

- Curve `Geometry` — Curve the strip follows
- Profile Curve `Geometry` — Cross-section of the strip
- Scale `Float` — Scale of the profile at each point
- Tilt `Float` — Rotation of the profile around the curve
- UV Map `String` — Name of the UV map to store
- UV Method `Menu` — How UV coordinates are generated
- Swap UV Channels `Boolean` — Swap the U and V channels
- Align To Active Camera `Boolean` — Turn the strip to face the active camera
- Fill Caps `Boolean` — If the profile spline is cyclic, fill the ends of the generated mesh with N-gons

**Outputs**

- Mesh `Geometry` — Generated strip mesh
- UVMap `Vector` — Generated UV coordinates


### A3D_UV Unwrap

**Description**

Unwraps a mesh's selected faces along seam edges using a selectable method, with margin, hole-filling, iteration, and no-flip controls.

**Inputs**

- Geometry `Geometry` — Geometry to unwrap
- Selection `Boolean` — Faces to participate in the unwrap operation
- Seam `Boolean` — Edges to mark where the mesh is "cut" for the purposes of unwrapping
- Margin `Float` — Space between islands
- Fill Holes `Boolean` — Virtually fill holes in mesh before unwrapping, to better avoid overlaps and preserve symmetry
- Method `Menu` — Unwrapping algorithm
- Iterations `Integer` — Number of iterations to run the SLIM solver for
- No Flip `Boolean` — Prevents flipping UVs

**Outputs**

- Geometry `Geometry` — Geometry with the unwrapped UVs
- UV `Vector` — UV coordinates between 0 and 1 for each face corner in the selected faces


### A3D_Vector to Angle

**Description**

Converts a 2D vector into its angle in radians.

**Inputs**

- Vector `Vector` — 2D vector to convert

**Outputs**

- Radians `Float` — Angle of the vector in radians


### A3D_Velocity Simulation

**Description**

Derives and writes a per-point velocity attribute across simulation steps, with damping.

**Inputs**

- Geometry `Geometry` — Geometry to simulate velocity on
- Damping `Float` — How much to damp the velocity
- Write Attribute `Boolean` — Store Named Attribute containing Velocity value
- Velocity Attribute `String` — Name of the attribute to store

**Outputs**

- Geometry `Geometry` — Geometry with the updated velocity
- Velocity `Vector` — Simulated velocity of each element


### A3D_View Transform

**Description**

Transforms a world-space position through a camera's view into view-space, clip-space (with W), and NDC coordinates.

**Inputs**

- Source `Menu` — Where the camera comes from
- Camera `Object` — Camera object to transform through
- Position `Vector` — Position to transform

**Outputs**

- View Space Position `Vector` — Position transformed to view space
- Clip Space Position `Vector` — Position transformed to clip space
- Clip Space W `Float` — Depth of transformed point in clip space
- NDC Position `Vector` — Position transformed to normalized device coordinates


### A3D_Volume of Mesh

**Description**

Computes the enclosed volume of a mesh.

**Inputs**

- Mesh `Geometry` — Mesh to measure

**Outputs**

- Volume `Float` — Volume enclosed by the mesh


### A3D_Wiggle

**Description**

Applies a physics-driven jiggle to a mesh using the motion of the object.
 
**Inputs**
 
- Geometry `Geometry` — The mesh to apply the wiggle to
- Influence `Float` — Per-point strength of the wobble
- Damping `Float` — How quickly the oscillation dies out
- Frequency `Float` — How fast the mesh oscillates, in Hz
- Gravity `Vector` — Constant acceleration in world space

**Outputs**

- Geometry `Geometry` — The input geometry with the simulated wobble applied to its point positions.


### A3D_XPBD Solver

**Description**

A full extended position-based dynamics (XPBD) cloth/soft-body solver. Supports fixed points, external force, damping, stretch stiffness, pretension, pressure, friction, and mesh collision, with pre/post-solve closures for custom constraint injection.

**Inputs**

- Geometry `Geometry` — Rope geometry to simulate
- Substeps `Integer` — Quality of simulation
- Fixed Points `Boolean` — Which points are fixed/immobile
- Animated `Boolean` — Are fixed points animated/updating every frame (use for rigs)
- External Force `Vector` — External force acting on simulation
- Damping `Float` — Velocity reduction (recommended >0)
- Stretch Stiffness `Float` — How much the rope resists stretching. High values require higher steps
- Pretension `Float` — Tension in the rope before simulation. Helps keep ropes stiff
- Pre Solve Closure `Closure` — Closure run before each solve step
- Post Solve Closure `Closure` — Closure run after each solve step
- Pressure `Boolean` — Enable pressure forces
- Pressure Coefficient `Float` — Strength of the pressure force
- Friction `Boolean` — Enable friction
- Friction Coefficient `Float` — Strength of the friction
- Collision `Boolean` — Enable collision
- Collision Substeps `Integer` — Number of substeps used for collision
- Collision Use Object `Boolean` — Collide with an object instead of a mesh
- Collision Object `Object` — Object to collide with
- Collision Mesh `Geometry` — Mesh to collide with

**Outputs**

- Geometry `Geometry` — Simulated rope geometry


### A3D_XPBD Solver Step

**Description**

A single time-stepped iteration of the XPBD solver, taking an explicit delta time and previous position and exposing the same stiffness/pressure/friction/collision controls as the full solver.

**Inputs**

- Delta Time `Float` — Time step of the simulation
- Geometry `Geometry` — Rope geometry to simulate
- Previous Position `Vector` — Positions from the previous step
- Substeps `Integer` — Number of substeps
- Fixed `Boolean` — Which points are fixed in place
- External Force `Vector` — External force acting on the simulation
- Damping `Float` — Velocity reduction applied each step
- Stiffness `Float` — How much the rope resists stretching
- Pretension `Float` — Tension in the rope before simulation
- Pressure `Boolean` — Enable pressure forces
- Pressure Coefficient `Float` — Strength of the pressure force
- Friction `Boolean` — Enable friction
- Friction Coefficient `Float` — Strength of the friction
- Collision `Boolean` — Enable collision
- Collision Substeps `Integer` — Number of substeps used for collision
- Collision Mesh `Geometry` — Mesh to collide with

**Outputs**

- Geometry `Geometry` — Simulated rope geometry
- Position `Vector` — Updated positions

