// **** WEAPON SHAPE KEY SHADER ****
// Contributors: Cybertron, SinsOfSeven
// Helpers: DiXiao, Leo, Silent
struct VertexAttributes {
  uint2 position;//8
  uint normal;//12
  uint color;//16
  uint texcoord0;//20
  uint texcoord1;//24
  uint tangent;//28
};

RWStructuredBuffer<VertexAttributes> rw_buffer : register(u0);
StructuredBuffer<VertexAttributes> base : register(t0);
StructuredBuffer<VertexAttributes> shapekey : register(t1);

Texture1D<float4> IniParams : register(t120);
#define key IniParams[0].x

float2 uintToHalf2ToFloat2(in uint a){
  return float2(f16tof32(a.x & 0xffff), f16tof32(a.x >> 0x10 & 0xffff));
}

uint float2ToHalf2ToUint(in float2 a){
  return uint(asuint(f32tof16(a.x)) | asuint(f32tof16(a.y)) << 0x10);
}

[numthreads(1, 1, 1)]
void main(uint3 threadID : SV_DispatchThreadID)
{
  float4 a,b,c;
  int i = threadID.x;
  uint2 r = shapekey[i].position,
  t = base[i].position,
  v = rw_buffer[i].position;
  a.xy = uintToHalf2ToFloat2(r.x);
  a.zw = uintToHalf2ToFloat2(r.y);
  b.xy = uintToHalf2ToFloat2(t.x);
  b.zw = uintToHalf2ToFloat2(t.y);
  c.xy = uintToHalf2ToFloat2(v.x);
  c.zw = uintToHalf2ToFloat2(v.y);

  c += (a-b)*key;

  rw_buffer[i].position.x = float2ToHalf2ToUint(c.xy);
  rw_buffer[i].position.y = float2ToHalf2ToUint(c.zw);
}

