#pragma once

#include "packet/PacketMgr.h"
#include "Rank.pb.h"
#include "SingleTon.hpp"

class Player;
class Packet;
extern std::unique_ptr<PacketMgr> g_pPacketMgr;
class HandleRank : public SingleTon<HandleRank>
{
public:
	enum ERank
	{
        MODULE_ID_RANK = 12,
        
	};
	// 在InitManager函数调用此函数进行消息注册
	HandleRank()
	{
		
	}
public:
	
};