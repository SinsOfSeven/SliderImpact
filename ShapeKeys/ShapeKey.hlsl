// **** SHAPE KEY SHADER ****
// Contributors: Cybertron, SinsOfSeven
// Helpers: DiXiao, Leo, Silent

struct VertexAttributes {
    float3 position;
    float3 normal;
    float4 tangent;
};

RWStructuredBuffer<VertexAttributes> rw_buffer : register(u5);
StructuredBuffer<VertexAttributes> base : register(t50);
StructuredBuffer<VertexAttributes> shapekey : register(t51);

Texture1D<float4> IniParams : register(t120);
#define key IniParams[88].x

float3 RotateVector(float3 p, float3 a, float3 o)
{ //Thanky DiXiao and Silent
  // position, angles, axis offset.
    p = p - o;
    float3x3 rotationMatrix = float3x3(
        cos(a.y) * cos(a.z), 
        sin(a.x) * sin(a.y) * cos(a.z) - cos(a.x) * sin(a.z), 
        cos(a.x) * sin(a.y) * cos(a.z) + sin(a.x) * sin(a.z),

        cos(a.y) * sin(a.z), 
        sin(a.x) * sin(a.y) * sin(a.z) + cos(a.x) * cos(a.z), 
        cos(a.x) * sin(a.y) * sin(a.z) - sin(a.x) * cos(a.z),

        -sin(a.y), 
        sin(a.x) * cos(a.y), 
        cos(a.x) * cos(a.y)
    );
    return mul(p, rotationMatrix)+o;
}

[numthreads(1, 1, 1)]
void main(uint3 threadID : SV_DispatchThreadID)
{
    uint i = threadID.x;
    VertexAttributes diff;
    diff.position = shapekey[i].position - base[i].position ;
    diff.normal = shapekey[i].normal - base[i].normal;
    diff.tangent = shapekey[i].tangent - base[i].tangent;
    rw_buffer[i].position += diff.position*key;
    rw_buffer[i].normal += diff.normal*key;
    rw_buffer[i].tangent += diff.tangent*key;
}
