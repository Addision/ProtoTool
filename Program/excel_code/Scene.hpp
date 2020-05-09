#pragma once

#include <memory>
#include <vector>
#include <string>
#include <unordered_map>

#include "json.h"
#include "JsonConfig.h"
#include "LogUtil.h"

class SceneRow
{
public:
	int id;                                           // ����id ��ͼidҲ�ǳ���id
	std::string comment;                              // ע�� 
	std::string name;                                 // ���� ����������
	std::string path;                                 // ��������·�� 
	int lines;                                        // ���� 0������ �����������÷��ߣ�Ĭ��2������
	int ismirror;                                     // �������� 0���Ǿ��� 1�����Ǿ���
	int type;                                         // �������� 1��ͨ���� 2���� 3����
	int server;                                       // ����������Ϸ�� 
	
};

class SceneTable
{
	typedef std::shared_ptr<SceneRow> ptr_row_type;
	typedef std::unordered_map<int, ptr_row_type> map_table_type;
	typedef std::vector<int> vec_type;	
private:
	vec_type m_keys;
	map_table_type	m_table;
public:
	static SceneTable* Instance()
	{
		static SceneTable instance;
		return &instance;
	}

	const SceneRow* GetRow(int key)
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
		return LoadJson("Scene.json");
	}

	bool ReLoad()
	{
		return ReLoadJson("Scene.json");
	}

	bool LoadJson(const std::string& jsonFile)
	{
		std::string loadfile = std::string(TABLE_PATH).append(jsonFile.c_str());
		if (!g_pConfig->Load(loadfile.c_str()))
		{
			CLOG_ERR << "load table Scene error" << CLOG_END;
			return false;
		}

		for (auto it = g_pConfig->m_Root.begin(); it != g_pConfig->m_Root.end(); ++it)
		{
			try
			{
				auto& r = (*it);
				ptr_row_type pRow(new SceneRow);
				SceneRow& row = *pRow;
                row.id = r["id"].asInt();
                row.comment = r["comment"].asString();
                row.name = r["name"].asString();
                row.path = r["path"].asString();
                row.lines = r["lines"].asInt();
                row.ismirror = r["ismirror"].asInt();
                row.type = r["type"].asInt();
                row.server = r["server"].asInt();

				m_table.emplace(row.id, pRow);
				m_keys.emplace_back(row.id);
			}
			catch (std::exception const& e)
			{
				CLOG_ERR << "read table Scene error," << e.what() << ":" << (*it)["id"].asInt() << CLOG_END;
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