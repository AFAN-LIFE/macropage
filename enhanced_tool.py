import os
import json
import datetime
import pandas as pd
import streamlit as st
from io import BytesIO
from functools import wraps


class FavoritesManager:
    def __init__(self, storage_file=".favorites.json"):
        self.storage_file = storage_file
        self.favorites = self._load_favorites()

    def _load_favorites(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_favorites(self):
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.favorites, f, ensure_ascii=False, indent=2)

    def add_favorite(self, item_name):
        if item_name not in self.favorites:
            self.favorites.append(item_name)
            self._save_favorites()
            return True
        return False

    def remove_favorite(self, item_name):
        if item_name in self.favorites:
            self.favorites.remove(item_name)
            self._save_favorites()
            return True
        return False

    def is_favorite(self, item_name):
        return item_name in self.favorites

    def get_favorites(self):
        return self.favorites.copy()


def get_favorites_manager():
    if 'favorites_manager' not in st.session_state:
        st.session_state.favorites_manager = FavoritesManager()
    return st.session_state.favorites_manager


class DataCollector:
    def __init__(self):
        self.collected_data = {}
        self.collected_filters = {}
        self._counter = 0

    def _get_unique_key(self, name):
        self._counter += 1
        return f"{name}_{self._counter}"

    def collect_data(self, name, df, filters=None, description=""):
        key = self._get_unique_key(name)
        if isinstance(df, pd.DataFrame) or isinstance(df, pd.Series):
            self.collected_data[key] = {
                "name": name,
                "data": df.copy() if isinstance(df, pd.DataFrame) else df.copy(),
                "filters": filters or {},
                "description": description,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            for filter_key, filter_value in (filters or {}).items():
                self.collected_filters[f"{name}: {filter_key}"] = filter_value
        return df

    def get_all_data(self):
        return self.collected_data.copy()

    def get_all_filters(self):
        return self.collected_filters.copy()

    def clear(self):
        self.collected_data = {}
        self.collected_filters = {}
        self._counter = 0


def get_data_collector():
    if 'data_collector' not in st.session_state:
        st.session_state.data_collector = DataCollector()
    return st.session_state.data_collector


def reset_data_collector():
    st.session_state.data_collector = DataCollector()


def collect_chart_data(name, filters=None, description=""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            collector = get_data_collector()
            if hasattr(args[0] if args else None, 'df'):
                df = getattr(args[0], 'df', None)
                if df is not None:
                    collector.collect_data(name, df, filters, description)
            return result
        return wrapper
    return decorator


class ComparisonMode:
    @staticmethod
    def wrap_chart(chart_func, chart_name, chart_key):
        st.markdown(f"**{chart_name}**")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            enable_comparison = st.checkbox(
                "开启对比模式", 
                key=f"comparison_mode_{chart_key}",
                value=False
            )
        
        if enable_comparison:
            main_col, compare_col = st.columns(2)
            with main_col:
                st.markdown("**主要视图**")
                with st.container():
                    chart_func()
            
            with compare_col:
                st.markdown("**对比视图**")
                with st.container():
                    st.info("对比模式 - 可独立选择时间范围")
                    chart_func()
        else:
            chart_func()


class ExportManager:
    def __init__(self):
        self.export_data = {}
        self.filter_conditions = {}
        self.data_collector = get_data_collector()

    def add_data(self, name, df, description=""):
        self.export_data[name] = {
            "data": df,
            "description": description
        }

    def add_filter_condition(self, key, value):
        self.filter_conditions[key] = value

    def _get_all_collected_data(self):
        all_data = {}
        all_data.update(self.export_data)
        
        collected = self.data_collector.get_all_data()
        for key, info in collected.items():
            all_data[key] = {
                "data": info["data"],
                "description": info.get("description", "")
            }
        
        return all_data

    def _get_all_filters(self):
        all_filters = {}
        all_filters.update(self.filter_conditions)
        all_filters.update(self.data_collector.get_all_filters())
        return all_filters

    def generate_excel_report(self):
        output = BytesIO()
        all_data = self._get_all_collected_data()
        all_filters = self._get_all_filters()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            if all_filters:
                filter_df = pd.DataFrame(
                    list(all_filters.items()),
                    columns=['筛选条件', '值']
                )
                filter_df.to_excel(writer, sheet_name='筛选条件', index=False)
            
            for name, info in all_data.items():
                safe_sheet_name = name[:31].replace('/', '_').replace('\\', '_').replace('*', '_').replace('?', '_').replace('[', '_').replace(']', '_').replace(':', '_')
                df = info["data"]
                if isinstance(df, pd.DataFrame):
                    df.to_excel(writer, sheet_name=safe_sheet_name, index=True)
                elif isinstance(df, pd.Series):
                    df.to_excel(writer, sheet_name=safe_sheet_name, index=True)
        
        output.seek(0)
        return output

    def generate_json_report(self):
        all_data = self._get_all_collected_data()
        all_filters = self._get_all_filters()
        
        export_dict = {
            "export_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "filter_conditions": all_filters,
            "datasets": {}
        }
        
        for name, info in all_data.items():
            df = info["data"]
            if isinstance(df, pd.DataFrame):
                export_dict["datasets"][name] = {
                    "description": info.get("description", ""),
                    "columns": list(df.columns),
                    "row_count": len(df),
                    "data": df.reset_index().to_dict(orient='records')
                }
            elif isinstance(df, pd.Series):
                export_dict["datasets"][name] = {
                    "description": info.get("description", ""),
                    "row_count": len(df),
                    "data": df.reset_index().to_dict(orient='records')
                }
        
        return json.dumps(export_dict, ensure_ascii=False, indent=2, default=str)
    
    def generate_csv_zip(self):
        import zipfile
        output = BytesIO()
        all_data = self._get_all_collected_data()
        all_filters = self._get_all_filters()
        
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
            if all_filters:
                filter_content = "筛选条件:\n"
                for key, value in all_filters.items():
                    filter_content += f"{key}: {value}\n"
                zf.writestr("筛选条件.txt", filter_content.encode('utf-8-sig'))
            
            for name, info in all_data.items():
                safe_name = name[:50].replace('/', '_').replace('\\', '_')
                df = info["data"]
                if isinstance(df, pd.DataFrame) or isinstance(df, pd.Series):
                    csv_content = df.to_csv(encoding='utf-8-sig')
                    zf.writestr(f"{safe_name}.csv", csv_content)
        
        output.seek(0)
        return output


def get_export_manager():
    if 'export_manager' not in st.session_state:
        st.session_state.export_manager = ExportManager()
    return st.session_state.export_manager


def reset_export_manager():
    st.session_state.export_manager = ExportManager()
    reset_data_collector()


def render_export_buttons():
    st.sidebar.markdown("#### 导出格式")
    
    col1, col2, col3 = st.sidebar.columns(3)
    
    with col1:
        excel_data = None
        try:
            if 'export_manager' in st.session_state:
                excel_data = st.session_state.export_manager.generate_excel_report()
        except:
            pass
        
        if excel_data:
            st.download_button(
                label="📥 Excel",
                data=excel_data,
                file_name=f"macropage_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                help="导出为Excel格式，包含筛选条件和所有数据表"
            )
        else:
            st.button("📥 Excel", use_container_width=True, disabled=True, help="请先选择看板查看数据")
    
    with col2:
        json_data = None
        try:
            if 'export_manager' in st.session_state:
                json_data = st.session_state.export_manager.generate_json_report()
        except:
            pass
        
        if json_data:
            st.download_button(
                label="📥 JSON",
                data=json_data,
                file_name=f"macropage_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
                help="导出为JSON格式，包含完整数据结构"
            )
        else:
            st.button("📥 JSON", use_container_width=True, disabled=True, help="请先选择看板查看数据")
    
    with col3:
        csv_data = None
        try:
            if 'export_manager' in st.session_state:
                csv_data = st.session_state.export_manager.generate_csv_zip()
        except:
            pass
        
        if csv_data:
            st.download_button(
                label="📥 CSV",
                data=csv_data,
                file_name=f"macropage_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                mime="application/zip",
                use_container_width=True,
                help="导出为CSV格式压缩包"
            )
        else:
            st.button("📥 CSV", use_container_width=True, disabled=True, help="请先选择看板查看数据")
    
    if st.sidebar.button("🔄 重置导出", use_container_width=True, help="清除当前收集的所有数据和筛选条件"):
        reset_export_manager()
        st.sidebar.success("已重置导出数据")
        time.sleep(0.3)
        st.rerun()
    
    st.sidebar.markdown("""
    <small>
    💡 提示：导出的数据是当前页面筛选后的结果，不是全量原始数据。
    选择看板后，数据会自动被收集用于导出。
    </small>
    """, unsafe_allow_html=True)


def show_export_info():
    collector = get_data_collector()
    collected = collector.get_all_data()
    filters = collector.get_all_filters()
    
    if collected or filters:
        with st.expander("📊 当前已收集的数据（用于导出）", expanded=False):
            if filters:
                st.markdown("**筛选条件：**")
                for key, value in filters.items():
                    st.text(f"  • {key}: {value}")
            
            if collected:
                st.markdown("**已收集的数据表：**")
                for key, info in collected.items():
                    row_count = len(info["data"]) if isinstance(info["data"], (pd.DataFrame, pd.Series)) else 0
                    st.text(f"  • {info['name']} ({row_count} 行)")


import time
