#pragma once

#include <memory>
#include <vector>
#include <string>
#include <unordered_map>

#include "json.h"
#include "JsonConfig.h"
#include "LogUtil.h"

class ActivityRow
{
public:
	int id;                                           // ����id �id
	std::string comment;                              // ע�� 
	int tab_id;                                       // ��ǩ��� �������ǩ
	int weight;                                       // Ȩ�� ��ǩ�б��ڵ���ʾȨ��
	int name_id;                                      // ����id �����id
	int describe_id;                                  // �����ı�id 
	int race_id;                                      // �Ƿ�������� �Ƿ���Ҫ�ж������������ʾ�Ի���ť,0��ʾ��1��ʾ��
	std::string main_icon;                            // ��ͼ���� 
	std::string sub_icon;                             // ��ͼ���� 
	int function_on;                                  // �Ƿ��� 0 ������ 1 ����
	int recommend;                                    // �Ƿ����Ƽ� 0 ������ 1 ����
	int call;                                         // ֧�ֿ����������� 0 ������ 1 ����
	int push;                                         // ֧�ֿ����������� 0 ������ 1 ����
	int open_type;                                    // ʱ������ 1 ȫ�쿪�� 2 ��ʱ����
	std::vector<int> open_in_week;                    // �����ܴ� ��ʱ����ʱʹ�� ������2|4
	std::vector<int> open_in_day;                     // ����ʱ�� ��ʱ����ʱʹ�� ���� 00:00 - 23:59�� 0|0|23|59
	int reset_type;                                   // ���ô������� 1 ÿ�� 2 ÿ��
	int level_min;                                    // ��͵ȼ����� 
	int player_min;                                   // ������������� 
	int active_value;                                 // ��Ծ�Ƚ��� ���ÿ���������Ļ�Ծ��
	int rounds_max;                                   // �ִ������� 
	int times_max;                                    // ���������� ��=������
	std::vector<int> drop_rounds;                     // ÿ�ֵ��佱�� ���㷽ʽ|�����id ��������㣺0���ʣ�1Ȩֵ��
	std::vector<int> drop_times;                      // ÿ�����佱�� ���㷽ʽ|�����id ��������㣺0���ʣ�1Ȩֵ��
	std::vector<int> drop_display;                    // ������ʾ 
	std::vector<int> scene_id;                        // ����id ��漰�����г���id
	int quest_id;                                     // ��¼����id ��¼��Ծ�ȵ�����id
	
};

class ActivityTable
{
	typedef std::shared_ptr<ActivityRow> ptr_row_type;
	typedef std::unordered_map<int, ptr_row_type> map_table_type;
	typedef std::vector<int> vec_type;	
private:
	vec_type m_keys;
	map_table_type	m_table;
public:
	static ActivityTable* Instance()
	{
		static ActivityTable instance;
		return &instance;
	}

	const ActivityRow* GetRow(int key)
	{
		map_table_type::iterator it = m_table.find(key);
		if (it == m_table.end())
		{
			return nullptr;
		}
		return it->second.get();
	}

	bool HasRow(int key)
	{
		return m_table.find(key) != m_table.end();
	}

	const vec_type& Keys() const
	{
		return m_keys;
	}

	const map_table_type& table() const
	{
		return m_table;
	}

	bool Load()
	{
		return LoadJson("Activity.json");
	}

	bool ReLoad()
	{
		return ReLoadJson("Activity.json");
	}

	bool LoadJson(const std::string& jsonFile)
	{
		std::string loadfile = std::string(TABLE_PATH).append(jsonFile.c_str());
		if (!g_pConfig->Load(loadfile.c_str()))
		{
			CLOG_ERR << "load table Activity error" << CLOG_END;
			return false;
		}

		for (auto it = g_pConfig->m_Root.begin(); it != g_pConfig->m_Root.end(); ++it)
		{
			try
			{
				auto& r = (*it);
				ptr_row_type pRow(new ActivityRow);
				ActivityRow& row = *pRow;
                row.id = r["id"].asInt();
                row.comment = r["comment"].asString();
                row.tab_id = r["tab_id"].asInt();
                row.weight = r["weight"].asInt();
                row.name_id = r["name_id"].asInt();
                row.describe_id = r["describe_id"].asInt();
                row.race_id = r["race_id"].asInt();
                row.main_icon = r["main_icon"].asString();
                row.sub_icon = r["sub_icon"].asString();
                row.function_on = r["function_on"].asInt();
                row.recommend = r["recommend"].asInt();
                row.call = r["call"].asInt();
                row.push = r["push"].asInt();
                row.open_type = r["open_type"].asInt();

                auto end_open_in_week = r["open_in_week"].end();
				auto begin_open_in_week = r["open_in_week"].end();
				for (auto it = begin_open_in_week; it != end_open_in_week; ++it)
				{
					row.open_in_week.emplace_back(it->asInt());
				}
            
                auto end_open_in_day = r["open_in_day"].end();
				auto begin_open_in_day = r["open_in_day"].end();
				for (auto it = begin_open_in_day; it != end_open_in_day; ++it)
				{
					row.open_in_day.emplace_back(it->asInt());
				}
                            row.reset_type = r["reset_type"].asInt();
                row.level_min = r["level_min"].asInt();
                row.player_min = r["player_min"].asInt();
                row.active_value = r["active_value"].asInt();
                row.rounds_max = r["rounds_max"].asInt();
                row.times_max = r["times_max"].asInt();

                auto end_drop_rounds = r["drop_rounds"].end();
				auto begin_drop_rounds = r["drop_rounds"].end();
				for (auto it = begin_drop_rounds; it != end_drop_rounds; ++it)
				{
					row.drop_rounds.emplace_back(it->asInt());
				}
            
                auto end_drop_times = r["drop_times"].end();
				auto begin_drop_times = r["drop_times"].end();
				for (auto it = begin_drop_times; it != end_drop_times; ++it)
				{
					row.drop_times.emplace_back(it->asInt());
				}
            
                auto end_drop_display = r["drop_display"].end();
				auto begin_drop_display = r["drop_display"].end();
				for (auto it = begin_drop_display; it != end_drop_display; ++it)
				{
					row.drop_display.emplace_back(it->asInt());
				}
            
                auto end_scene_id = r["scene_id"].end();
				auto begin_scene_id = r["scene_id"].end();
				for (auto it = begin_scene_id; it != end_scene_id; ++it)
				{
					row.scene_id.emplace_back(it->asInt());
				}
                            row.quest_id = r["quest_id"].asInt();

				m_table.emplace(row.id, pRow);
				m_keys.emplace_back(row.id);
			}
			catch (std::exception const& e)
			{
				CLOG_ERR << "read table Activity error," << e.what() << ":" << (*it)["id"].asInt() << CLOG_END;
				return false;
			}
		}
		return true;
	}

	bool ReLoadJson(const std::string& jsonFile)
	{
		m_keys.clear();
		m_table.clear();
		return LoadJson(jsonFile);
	}

};