#pragma once

#include "SingleTon.hpp"
#include "packet/PacketMgr.h"

class Player;
class Packet;
extern std::unique_ptr<PacketMgr> g_pPacketMgr;
class HandleGate : public SingleTon<HandleGate>
{
public:
	enum EGate
	{
		MODULE_ID_GATE = 12,
	};
	HandleGate()
	{

	}
private:
};