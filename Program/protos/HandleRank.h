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
        RPC_RANK_RANKFIGHT_REQ = 1201,
	};
	// 在InitManager函数调用此函数进行消息注册
	HandleRank()
	{
		g_pPacketMgr->RegisterHandle(RPC_RANK_RANKFIGHT_REQ, HandleRank::RankFightReq);
		g_pPacketMgr->RegisterPacket(RPC_RANK_RANKFIGHT_REQ, new CPacket<Rank_RankFightReq>());
	}
public:
	static int RankFightReq(Player* player, Packet* packet);
};