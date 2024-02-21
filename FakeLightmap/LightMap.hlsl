// **** SHAPE KEY SHADER ****
// Contributors: Cybertron, SinsOfSeven
// Helpers: DiXiao, Leo, Silent

RWTexture2D<float4> tex : register(u5);
//Texture2D<float4> base : register(t50);

Texture1D<float4> IniParams : register(t120);
#define color IniParams[87].xyzw

[numthreads(1, 4, 4)]
void main(uint3 threadID : SV_DispatchThreadID)
{
    tex[threadID.yz] = color;
}
