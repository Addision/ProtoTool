#pragma once

#include "packet/PacketMgr.h"
#include "Chat.pb.h"
#include "SingleTon.hpp"

class Player;
class Packet;
extern std::unique_ptr<PacketMgr> g_pPacketMgr;
class HandleChat : public SingleTon<HandleChat>
{
public:
	enum EChat
	{
        MODULE_ID_CHAT = 11,
        RPC_CHAT_CHATTOONE_REQ = 1101,
		RPC_CHAT_CHATTOALL_NOTIFY = 1102,
	};
	// 在InitManager函数调用此函数进行消息注册
	HandleChat()
	{
		g_pPacketMgr->RegisterHandle(RPC_CHAT_CHATTOONE_REQ, HandleChat::ChatToOneReq);
		g_pPacketMgr->RegisterPacket(RPC_CHAT_CHATTOONE_REQ, new CPacket<Chat_ChatToOneReq>());
		g_pPacketMgr->RegisterHandle(RPC_CHAT_CHATTOALL_NOTIFY, HandleChat::ChatToAllReq);
		g_pPacketMgr->RegisterPacket(RPC_CHAT_CHATTOALL_NOTIFY, new CPacket<Chat_ChatToAllReq>());
	}
public:
	static int ChatToOneReq(Player* player, Packet* packet);
	static int ChatToAllReq(Player* player, Packet* packet);
};