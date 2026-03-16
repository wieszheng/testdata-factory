import { useState, useEffect } from 'react'
import { 
  Sparkles, Phone, Mail, CreditCard, Download, Copy, Check,
  Settings, Database, Wand2, ChevronDown, Globe, MapPin,
  Calendar, User, Link, AlertCircle, Code, Building, Briefcase,
  DollarSign, Palette, Fingerprint, Key, FileText, Table, FileJson,
  Server, ChevronRight, X, Loader2, FileCode, Sun, Moon
} from 'lucide-react'
import { ToastProvider, useToast } from './components/ui/toast-provider'

const API_BASE = 'http://localhost:8001/api'

interface DataType {
  key: string
  label: string
  icon: React.ReactNode
}

const DATA_TYPES: DataType[] = [
  { key: 'phone', label: '手机号', icon: <Phone className="w-3 h-3" /> },
  { key: 'email', label: '邮箱', icon: <Mail className="w-3 h-3" /> },
  { key: 'id_card', label: '身份证号', icon: <CreditCard className="w-3 h-3" /> },
  { key: 'name', label: '姓名', icon: <User className="w-3 h-3" /> },
  { key: 'company', label: '公司名', icon: <Building className="w-3 h-3" /> },
  { key: 'position', label: '职位', icon: <Briefcase className="w-3 h-3" /> },
  { key: 'ip', label: 'IP地址', icon: <Globe className="w-3 h-3" /> },
  { key: 'address', label: '地址', icon: <MapPin className="w-3 h-3" /> },
  { key: 'date', label: '日期', icon: <Calendar className="w-3 h-3" /> },
  { key: 'bank_card', label: '银行卡号', icon: <CreditCard className="w-3 h-3" /> },
  { key: 'price', label: '价格', icon: <DollarSign className="w-3 h-3" /> },
  { key: 'color', label: '颜色', icon: <Palette className="w-3 h-3" /> },
  { key: 'url', label: 'URL', icon: <Link className="w-3 h-3" /> },
  { key: 'uuid', label: 'UUID', icon: <Fingerprint className="w-3 h-3" /> },
  { key: 'username', label: '用户名', icon: <User className="w-3 h-3" /> },
  { key: 'password', label: '密码', icon: <Key className="w-3 h-3" /> },
  { key: 'sentence', label: '句子', icon: <FileText className="w-3 h-3" /> },
]

const TYPE_LABELS: Record<string, string> = {
  phone: '手机号', email: '邮箱', id_card: '身份证号', name: '姓名',
  company: '公司名', position: '职位', ip: 'IP地址', address: '地址',
  date: '日期', datetime: '日期时间', bank_card: '银行卡号',
  price: '价格', color: '颜色', url: 'URL', uuid: 'UUID',
  username: '用户名', password: '密码', sentence: '句子',
}

interface RegexTemplate { name: string; pattern: string }
interface DataItem { [key: string]: string }
interface DbConfig { db_type: string; host: string; port: number; username: string; password: string; database: string }

function AppContent() {
  const [count, setCount] = useState(10)
  const [selectedTypes, setSelectedTypes] = useState<string[]>(['phone', 'email', 'name'])
  const [data, setData] = useState<DataItem[]>([])
  const [columns, setColumns] = useState<string[]>([])
  const [copied, setCopied] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  // 自定义正则模态框
  const [showRegexModal, setShowRegexModal] = useState(false)
  const [regexPattern, setRegexPattern] = useState('')
  const [regexName, setRegexName] = useState('自定义字段')
  const [templates, setTemplates] = useState<RegexTemplate[]>([])
  const [regexData, setRegexData] = useState<string[]>([])
  const [viewMode, setViewMode] = useState<'table' | 'json'>('table')
  
  // 主题切换
  const [isDark, setIsDark] = useState(true)
  
  // 数据库相关
  const [showDbPanel, setShowDbPanel] = useState(false)
  const [dbConfig, setDbConfig] = useState<DbConfig>({ db_type: 'mysql', host: 'localhost', port: 3306, username: 'root', password: '', database: '' })
  const [dbConnecting, setDbConnecting] = useState(false)
  const [dbTables, setDbTables] = useState<string[]>([])
  const [selectedTable, setSelectedTable] = useState('')
  const [dbError, setDbError] = useState<string | null>(null)
  const [dbSuccess, setDbSuccess] = useState<string | null>(null)
  
  // Toast 提示
  const { toast } = useToast()

  useEffect(() => {
    fetch(`${API_BASE}/templates`)
      .then(res => res.json())
      .then(result => setTemplates(result.templates || []))
      .catch(() => {})
  }, [])

  const toggleType = (key: string) => {
    setSelectedTypes(prev => 
      prev.includes(key) ? prev.filter(t => t !== key) : [...prev, key]
    )
  }

  const handleGenerate = async () => {
    if (selectedTypes.length === 0) { setError('请至少选择一种数据类型'); return }
    setIsGenerating(true); setError(null)
    
    try {
      const response = await fetch(`${API_BASE}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ count, types: selectedTypes }),
      })
      const result = await response.json()
      setData(result.data); setColumns(result.types); setRegexData([])
    } catch { setError('生成失败') }
    finally { setIsGenerating(false) }
  }

  const handleRegexGenerate = async () => {
    if (!regexPattern.trim()) { setError('请输入正则表达式'); return }
    setIsGenerating(true); setError(null)
    
    try {
      const response = await fetch(`${API_BASE}/regex`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ count, pattern: regexPattern, name: regexName }),
      })
      const result = await response.json()
      if (result.success) { setRegexData(result.data); setData([]); setColumns([]) }
      else { setError('正则表达式格式错误') }
    } catch { setError('生成失败') }
    finally { setIsGenerating(false) }
  }

  const handleDbConnect = async () => {
    setDbConnecting(true); setDbError(null); setDbSuccess(null); setDbTables([])
    
    try {
      const response = await fetch(`${API_BASE}/database/connect`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dbConfig),
      })
      const result = await response.json()
      
      if (result.success) {
        setDbTables(result.tables)
        setDbSuccess(result.message)
        toast({ description: result.message, variant: 'success' })
      } else {
        setDbError(result.message)
        toast({ description: result.message, variant: 'error' })
      }
    } catch (e) {
      const errorMsg = '连接失败，请检查后端服务是否运行'
      setDbError(errorMsg)
      toast({ description: errorMsg, variant: 'error' })
    } finally {
      setDbConnecting(false)
    }
  }

  const handleDbGenerate = async (tableName: string) => {
    setIsGenerating(true); setError(null)
    
    try {
      const response = await fetch(`${API_BASE}/database/generate?table_name=${tableName}&count=${count}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dbConfig),
      })
      const result = await response.json()
      
      if (result.success) {
        setData(result.data)
        setColumns(result.columns)
        setRegexData([])
        setShowDbPanel(false)
      } else {
        setError('生成失败')
      }
    } catch { setError('生成失败') }
    finally { setIsGenerating(false) }
  }

  const handleCopy = () => {
    let text = ''
    if (data.length > 0) text = data.map(row => columns.map(col => row[col] || '').join('\t')).join('\n')
    else if (regexData.length > 0) text = regexData.join('\n')
    if (text) { navigator.clipboard.writeText(text); setCopied(true); setTimeout(() => setCopied(false), 2000) }
  }

  const handleExportCSV = () => {
    let csv = ''
    if (data.length > 0) csv = columns.map(c => TYPE_LABELS[c] || c).join(',') + '\n' + data.map(row => columns.map(col => row[col] || '').join(',')).join('\n')
    else if (regexData.length > 0) csv = regexName + '\n' + regexData.join('\n')
    if (csv) {
      const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a'); a.href = url; a.download = `test_data_${Date.now()}.csv`; a.click()
      URL.revokeObjectURL(url)
    }
  }

  const handleExportJSON = () => {
    let json = ''
    if (data.length > 0) json = JSON.stringify(data.map(row => { const item: Record<string, string> = {}; columns.forEach(col => { item[TYPE_LABELS[col] || col] = row[col] || '' }); return item }), null, 2)
    else if (regexData.length > 0) json = JSON.stringify(regexData.map(v => ({ [regexName]: v })), null, 2)
    if (json) {
      const blob = new Blob([json], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a'); a.href = url; a.download = `test_data_${Date.now()}.json`; a.click()
      URL.revokeObjectURL(url)
    }
  }

  // SQL 导出相关
  const [showSqlModal, setShowSqlModal] = useState(false)
  const [sqlTableName, setSqlTableName] = useState('test_table')

  const handleExportSQL = () => {
    if (data.length === 0 && regexData.length === 0) {
      toast({ description: '没有数据可导出', variant: 'warning' })
      return
    }
    setShowSqlModal(true)
  }

  const generateSQL = () => {
    if (data.length > 0) {
      // 多列数据
      const colNames = columns.map(col => TYPE_LABELS[col] || col)
      const values = data.map(row => {
        const vals = columns.map(col => {
          const val = row[col] || ''
          return `'${val.replace(/'/g, "''")}'`  // 转义单引号
        })
        return `(${vals.join(', ')})`
      })
      
      const sql = `-- 插入 ${data.length} 条记录到表 ${sqlTableName}
INSERT INTO ${sqlTableName} (${colNames.join(', ')}) VALUES
${values.join(',\n')};`
      return sql
    } else if (regexData.length > 0) {
      // 单列数据
      const values = regexData.map(val => `('${val.replace(/'/g, "''")}')`)
      
      const sql = `-- 插入 ${regexData.length} 条记录到表 ${sqlTableName}
INSERT INTO ${sqlTableName} (${regexName}) VALUES
${values.join(',\n')};`
      return sql
    }
    return ''
  }

  const handleDownloadSQL = () => {
    const sql = generateSQL()
    if (sql) {
      const blob = new Blob([sql], { type: 'text/plain;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `insert_${sqlTableName}_${Date.now()}.sql`
      a.click()
      URL.revokeObjectURL(url)
      setShowSqlModal(false)
      toast({ description: 'SQL 文件已下载', variant: 'success' })
    }
  }

  return (
    <div data-theme={isDark ? 'dark' : 'light'} className={`min-h-screen transition-colors duration-300 ${isDark ? 'bg-[#0f1419] text-white' : 'bg-gray-50 text-gray-900'}`}>
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className={`absolute top-0 left-1/4 w-96 h-96 rounded-full blur-3xl ${isDark ? 'bg-[#ff6b4a] opacity-10' : 'bg-[#ff6b4a] opacity-20'}`} />
        <div className={`absolute bottom-0 right-1/4 w-96 h-96 rounded-full blur-3xl ${isDark ? 'bg-[#5a5eff] opacity-10' : 'bg-blue-400 opacity-20'}`} />
      </div>

      <nav className={`sticky top-0 z-50 backdrop-blur-xl border-b ${isDark ? 'bg-[#0f1419]/80 border-white/10' : 'bg-white/80 border-gray-200'}`}>
        <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className={`p-1.5 rounded-lg ${isDark ? 'bg-gradient-to-br from-[#ff6b4a] to-[#ff8f7a]' : 'bg-gradient-to-br from-[#ff6b4a] to-[#ff8f7a]'}`}><Sparkles className="w-4 h-4 text-white" /></div>
            <div>
              <h1 className={`text-sm font-bold ${isDark ? 'gradient-text-warm' : 'text-[#ff6b4a]'}`}>TestData Factory</h1>
              <p className={`text-[10px] ${isDark ? 'text-[#94a3b8]' : 'text-gray-500'}`}>智能测试数据生成器</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button 
              onClick={() => setIsDark(!isDark)}
              className={`p-1.5 rounded-lg transition-colors ${isDark ? 'bg-white/10 text-yellow-400 hover:bg-white/20' : 'bg-gray-200 text-gray-600 hover:bg-gray-300'}`}
              title={isDark ? '切换亮色模式' : '切换深色模式'}
            >
              {isDark ? <Sun className="w-3.5 h-3.5" /> : <Moon className="w-3.5 h-3.5" />}
            </button>
            <a href="http://localhost:8000/docs" target="_blank" className="text-[10px] text-[#94a3b8] hover:text-[#ff6b4a] flex items-center gap-1">
              <Settings className="w-3 h-3" /> API
            </a>
          </div>
        </div>
      </nav>

      <section className={`py-4 px-4 ${isDark ? '' : 'bg-gray-50'}`}>
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-xl font-bold mb-1"><span className="gradient-text-warm">测试数据</span><span className={isDark ? 'text-white' : 'text-gray-900'}> 一键生成</span></h2>
          <p className={`text-xs ${isDark ? 'text-[#94a3b8]' : 'text-gray-500'}`}>17 种数据类型 · 自定义正则 · 数据库逆向 · 导出 CSV/JSON/SQL</p>
        </div>
      </section>

      <section className="pb-8 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="glass-card p-3 sm:p-4 mb-3">
            {/* 数据类型选择 */}
            <div className="mb-3">
              <label className={`block text-[10px] font-medium mb-1.5 ${isDark ? 'text-[#94a3b8]' : 'text-gray-500'}`}>选择数据类型</label>
              <div className="flex flex-wrap gap-1">
                {DATA_TYPES.map(type => (
                  <button key={type.key} onClick={() => toggleType(type.key)}
                    className={`type-btn text-xs ${selectedTypes.includes(type.key) ? 'active' : ''}`}>
                    {type.icon}<span className="ml-0.5">{type.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* 添加自定义正则规则按钮 */}
            <div className="mb-3">
              <button 
                onClick={() => setShowRegexModal(true)} 
                className={`w-full py-2.5 rounded-lg border-2 border-dashed transition-colors flex items-center justify-center gap-2 text-[11px] font-medium ${
                  isDark 
                    ? 'border-white/20 text-[#5a5eff] hover:bg-[#5a5eff]/10 hover:border-[#5a5eff]/40' 
                    : 'border-gray-300 text-[#4a3df0] hover:bg-[#4a3df0]/5 hover:border-[#4a3df0]/40'
                }`}
              >
                <Code className="w-3.5 h-3.5" />
                添加自定义正则规则
              </button>
            </div>

            <div className={`mb-3 h-px ${isDark ? 'bg-gradient-to-r from-transparent via-[#ff6b4a]/50 to-transparent' : 'bg-gray-200'}`} />

            {error && <div className="mb-3 p-2 bg-red-500/10 border border-red-500/30 rounded flex items-center gap-2"><AlertCircle className="w-3 h-3 text-red-400" /><p className="text-[10px] text-red-400">{error}</p></div>}

            {/* 底部操作栏 */}
            <div className={`flex items-center justify-between pt-3 mt-3 border-t ${isDark ? 'border-white/10' : 'border-gray-200'}`}>
              <div className="flex items-center gap-2">
                <label className={`text-[10px] ${isDark ? 'text-[#94a3b8]' : 'text-gray-500'}`}>生成数量</label>
                <input type="number" value={count} onChange={(e) => setCount(Math.max(1, Math.min(1000, parseInt(e.target.value) || 1)))} min={1} max={1000} className={`text-center text-xs font-semibold py-1 px-2 rounded w-16 ${isDark ? 'input-glass' : 'border border-gray-300 bg-white'}`} />
                <span className={`text-[10px] ${isDark ? 'text-[#94a3b8]' : 'text-gray-400'}`}>条</span>
              </div>
              <button onClick={handleGenerate} disabled={isGenerating || selectedTypes.length === 0} className={`flex items-center justify-center gap-1 disabled:opacity-50 h-[28px] px-3 text-[10px] rounded font-medium ${isDark ? 'btn-primary' : 'bg-gradient-to-r from-[#ff6b4a] to-[#ff8f7a] text-white shadow hover:shadow-md transition-shadow'}`}>
                {isGenerating ? <><div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />生成中</> : <><Sparkles className="w-3 h-3" />立即生成</>}
              </button>
            </div>
          </div>

          {/* 数据库逆向面板 */}
          <div className="glass-card p-3 sm:p-4 mb-3">
            <button onClick={() => setShowDbPanel(!showDbPanel)} className="w-full flex items-center justify-between text-[10px] font-medium text-[#05c4a5] hover:text-[#00d4b5]">
              <div className="flex items-center gap-2">
                <Server className="w-3.5 h-3.5" />
                <span>数据库逆向解析</span>
                <span className={isDark ? 'text-[#94a3b8] font-normal' : 'text-gray-500 font-normal'}>从数据库表结构自动生成数据</span>
              </div>
              <ChevronDown className={`w-3.5 h-3.5 transition-transform ${showDbPanel ? 'rotate-180' : ''}`} />
            </button>
            
            {showDbPanel && (
              <div className="mt-3 space-y-2">
                {/* 数据库类型选择 */}
                <div className="flex gap-1">
                  {['mysql', 'postgresql', 'sqlite'].map(type => (
                    <button key={type} onClick={() => setDbConfig(prev => ({ ...prev, db_type: type, port: type === 'mysql' ? 3306 : type === 'postgresql' ? 5432 : 0 }))}
                      className={`flex-1 py-1 text-[10px] rounded transition-colors ${
                        dbConfig.db_type === type 
                          ? 'bg-[#05c4a5]/20 text-[#05c4a5] border border-[#05c4a5]/30' 
                          : isDark 
                            ? 'bg-white/5 text-[#94a3b8] hover:bg-white/10 border border-transparent' 
                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200 border border-transparent'
                      }`}>
                      {type === 'mysql' ? 'MySQL' : type === 'postgresql' ? 'PostgreSQL' : 'SQLite'}
                    </button>
                  ))}
                </div>
                
                {/* 连接信息 */}
                <div className="grid grid-cols-3 gap-1.5">
                  <div>
                    <label className={`block text-[9px] mb-0.5 ${isDark ? 'text-[#94a3b8]' : 'text-gray-500'}`}>主机</label>
                    <input type="text" value={dbConfig.host} onChange={(e) => setDbConfig(prev => ({ ...prev, host: e.target.value }))} 
                      placeholder="localhost" className={`text-[10px] py-1 px-2 w-full rounded ${isDark ? 'input-glass' : 'border border-gray-300 bg-gray-50'}`} />
                  </div>
                  <div>
                    <label className={`block text-[9px] mb-0.5 ${isDark ? 'text-[#94a3b8]' : 'text-gray-500'}`}>端口</label>
                    <input type="number" value={dbConfig.port} onChange={(e) => setDbConfig(prev => ({ ...prev, port: parseInt(e.target.value) || 3306 }))}
                      placeholder="3306" className={`text-[10px] py-1 px-2 w-full rounded ${isDark ? 'input-glass' : 'border border-gray-300 bg-gray-50'}`} />
                  </div>
                  <div>
                    <label className={`block text-[9px] mb-0.5 ${isDark ? 'text-[#94a3b8]' : 'text-gray-500'}`}>{dbConfig.db_type === 'sqlite' ? '文件路径' : '数据库'}</label>
                    <input type="text" value={dbConfig.database} onChange={(e) => setDbConfig(prev => ({ ...prev, database: e.target.value }))}
                      placeholder={dbConfig.db_type === 'sqlite' ? '/path/to/db.sqlite' : 'database_name'} className={`text-[10px] py-1 px-2 w-full rounded ${isDark ? 'input-glass' : 'border border-gray-300 bg-gray-50'}`} />
                  </div>
                </div>
                
                {/* 用户名密码（非 SQLite） */}
                {dbConfig.db_type !== 'sqlite' && (
                  <div className="grid grid-cols-2 gap-1.5">
                    <div>
                      <label className={`block text-[9px] mb-0.5 ${isDark ? 'text-[#94a3b8]' : 'text-gray-500'}`}>用户名</label>
                      <input type="text" value={dbConfig.username} onChange={(e) => setDbConfig(prev => ({ ...prev, username: e.target.value }))}
                        placeholder="root" className={`text-[10px] py-1 px-2 w-full rounded ${isDark ? 'input-glass' : 'border border-gray-300 bg-gray-50'}`} />
                    </div>
                    <div>
                      <label className={`block text-[9px] mb-0.5 ${isDark ? 'text-[#94a3b8]' : 'text-gray-500'}`}>密码</label>
                      <input type="password" value={dbConfig.password} onChange={(e) => setDbConfig(prev => ({ ...prev, password: e.target.value }))}
                        placeholder="••••••••" className={`text-[10px] py-1 px-2 w-full rounded ${isDark ? 'input-glass' : 'border border-gray-300 bg-gray-50'}`} />
                    </div>
                  </div>
                )}
                
                {/* 连接按钮 */}
                <button onClick={handleDbConnect} disabled={dbConnecting || !dbConfig.database}
                  className="w-full py-1.5 bg-gradient-to-r from-[#05c4a5] to-[#009e87] text-white rounded text-[10px] font-medium disabled:opacity-50 flex items-center justify-center gap-1">
                  {dbConnecting ? <><Loader2 className="w-3 h-3 animate-spin" />连接中...</> : <><Server className="w-3 h-3" />连接数据库</>}
                </button>
                
                {/* 提示信息 */}
                {dbSuccess && (
                  <div className="flex items-center gap-1.5 px-2 py-1.5 bg-[#05c4a5]/10 border border-[#05c4a5]/30 rounded">
                    <Check className="w-3 h-3 text-[#05c4a5]" />
                    <p className="text-[10px] text-[#05c4a5]">{dbSuccess}</p>
                  </div>
                )}
                {dbError && (
                  <div className="flex items-center gap-1.5 px-2 py-1.5 bg-red-500/10 border border-red-500/30 rounded">
                    <AlertCircle className="w-3 h-3 text-red-400" />
                    <p className="text-[10px] text-red-400">{dbError}</p>
                  </div>
                )}
                
                {/* 表列表 */}
                {dbTables.length > 0 && (
                  <div className="border border-white/10 rounded overflow-hidden">
                    <div className="px-2 py-1 bg-white/5 text-[9px] text-[#94a3b8]">发现 {dbTables.length} 个表</div>
                    <div className="max-h-[120px] overflow-y-auto">
                      {dbTables.map(table => (
                        <button key={table} onClick={() => handleDbGenerate(table)}
                          className="w-full px-2 py-1.5 text-left text-[10px] text-[#94a3b8] hover:bg-[#05c4a5]/10 hover:text-[#05c4a5] flex items-center justify-between border-t border-white/5">
                          <span className="truncate">{table}</span>
                          <ChevronRight className="w-3 h-3 flex-shrink-0" />
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* 结果展示 */}
          {(data.length > 0 || regexData.length > 0) && (
            <div className="glass-card p-3 sm:p-4 mb-3">
              <div className={`flex items-center justify-between gap-2 mb-3 pb-2 border-b ${isDark ? 'border-white/10' : 'border-gray-200'}`}>
                <div>
                  <h3 className={`font-bold text-xs ${isDark ? 'text-white' : 'text-gray-900'}`}>结果</h3>
                  <p className={`text-[10px] ${isDark ? 'text-[#94a3b8]' : 'text-gray-500'}`}>{data.length > 0 ? `${data.length} 条 · ${columns.length} 字段` : `${regexData.length} 条`}</p>
                </div>
                <div className="flex items-center gap-1">
                  <div className={`flex rounded p-0.5 mr-1 ${isDark ? 'bg-white/5' : 'bg-gray-100'}`}>
                    <button onClick={() => setViewMode('table')} className={`p-1 rounded transition-colors ${viewMode === 'table' ? 'bg-[#ff6b4a]/20 text-[#ff6b4a]' : isDark ? 'text-[#94a3b8] hover:text-white' : 'text-gray-400 hover:text-gray-600'}`}><Table className="w-3.5 h-3.5" /></button>
                    <button onClick={() => setViewMode('json')} className={`p-1 rounded transition-colors ${viewMode === 'json' ? 'bg-[#ff6b4a]/20 text-[#ff6b4a]' : isDark ? 'text-[#94a3b8] hover:text-white' : 'text-gray-400 hover:text-gray-600'}`}><FileJson className="w-3.5 h-3.5" /></button>
                  </div>
                  <button onClick={handleCopy} className={`py-1 px-1.5 rounded transition-colors ${isDark ? 'btn-secondary' : 'bg-gray-100 hover:bg-gray-200 text-gray-600'}`}>{copied ? <Check className="w-3 h-3 text-green-400" /> : <Copy className="w-3 h-3" />}</button>
                  <button onClick={handleExportCSV} className={`py-1 px-1.5 rounded transition-colors ${isDark ? 'btn-secondary' : 'bg-gray-100 hover:bg-gray-200 text-gray-600'}`} title="导出CSV"><Download className="w-3 h-3" /></button>
                  <button onClick={handleExportJSON} className={`py-1 px-1.5 rounded transition-colors ${isDark ? 'btn-secondary' : 'bg-gray-100 hover:bg-gray-200 text-gray-600'}`} title="导出JSON"><FileJson className="w-3 h-3" /></button>
                  <button onClick={handleExportSQL} className={`py-1 px-1.5 rounded transition-colors ${isDark ? 'btn-secondary' : 'bg-gray-100 hover:bg-gray-200 text-gray-600'}`} title="导出SQL"><FileCode className="w-3 h-3" /></button>
                </div>
              </div>

              {viewMode === 'table' ? (
                <div className="overflow-x-auto overflow-y-auto max-h-[350px]">
                  {data.length > 0 ? (
                    <table className={`min-w-full ${isDark ? 'table-glass' : 'text-gray-900'}`}>
                      <thead className={`sticky top-0 ${isDark ? '' : 'bg-gray-100'}`}><tr>{columns.map(col => <th key={col} className={`text-[10px] py-1.5 px-2 whitespace-nowrap font-medium ${isDark ? '' : 'text-left'}`}>{TYPE_LABELS[col] || col}</th>)}</tr></thead>
                      <tbody>{data.map((row, i) => <tr key={i} className={isDark ? '' : 'border-b border-gray-100'}>{columns.map(col => <td key={col} className={`text-[10px] py-1.5 px-2 whitespace-nowrap ${isDark ? '' : 'text-gray-700'}`}>{row[col] || '-'}</td>)}</tr>)}</tbody>
                    </table>
                  ) : (
                    <table className={`min-w-full ${isDark ? 'table-glass' : 'text-gray-900'}`}>
                      <thead className={`sticky top-0 ${isDark ? '' : 'bg-gray-100'}`}><tr><th className={`text-[10px] py-1.5 px-2 font-medium ${isDark ? '' : 'text-left'}`}>{regexName}</th></tr></thead>
                      <tbody>{regexData.map((v, i) => <tr key={i} className={isDark ? '' : 'border-b border-gray-100'}><td className={`text-[10px] py-1.5 px-2 ${isDark ? '' : 'text-gray-700'}`}>{v}</td></tr>)}</tbody>
                    </table>
                  )}
                </div>
              ) : (
                <div className={`overflow-auto max-h-[350px] rounded-lg p-2 ${isDark ? 'bg-black/20' : 'bg-gray-100'}`}>
                  <pre className={`text-[10px] font-mono whitespace-pre-wrap break-all ${isDark ? 'text-[#94a3b8]' : 'text-gray-700'}`}>
                    {data.length > 0 ? JSON.stringify(data.map(row => { const item: Record<string, string> = {}; columns.forEach(col => { item[TYPE_LABELS[col] || col] = row[col] || '' }); return item }), null, 2) : JSON.stringify(regexData.map(v => ({ [regexName]: v })), null, 2)}
                  </pre>
                </div>
              )}
            </div>
          )}
        </div>
      </section>

      {/* 自定义正则规则模态框 */}
      {showRegexModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className={`p-4 w-full max-w-md mx-4 rounded-xl ${isDark ? 'glass-card' : 'bg-white shadow-2xl border border-gray-200'}`}>
            <div className="flex items-center justify-between mb-4">
              <h3 className={`text-sm font-bold flex items-center gap-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                <Code className="w-4 h-4 text-[#5a5eff]" />
                自定义正则规则
              </h3>
              <button onClick={() => setShowRegexModal(false)} className={isDark ? 'text-[#94a3b8] hover:text-white' : 'text-gray-400 hover:text-gray-600'}>
                <X className="w-4 h-4" />
              </button>
            </div>
            
            <div className="space-y-3">
              <div className="space-y-1.5">
                <label className={`text-[10px] font-medium ${isDark ? 'text-[#94a3b8]' : 'text-gray-600'}`}>
                  字段名称
                </label>
                <input 
                  type="text" 
                  value={regexName} 
                  onChange={(e) => setRegexName(e.target.value)} 
                  placeholder="如：订单号"
                  className={`h-9 text-[11px] rounded-md border px-3 w-full transition-colors ${
                    isDark 
                      ? 'bg-white/5 border-white/10 text-white placeholder:text-white/30 focus:border-[#5a5eff] focus:outline-none' 
                      : 'bg-white border-gray-300 text-gray-900 placeholder:text-gray-400 focus:border-[#4a3df0] focus:outline-none'
                  }`} 
                />
              </div>
              
              <div className="space-y-1.5">
                <label className={`text-[10px] font-medium ${isDark ? 'text-[#94a3b8]' : 'text-gray-600'}`}>
                  选择模板（可选）
                </label>
                <select 
                  value={regexPattern} 
                  onChange={(e) => { 
                    setRegexPattern(e.target.value); 
                    const t = templates.find(t => t.pattern === e.target.value); 
                    if (t) setRegexName(t.name);
                  }} 
                  className={`h-9 text-[11px] rounded-md border px-3 w-full transition-colors ${
                    isDark 
                      ? 'bg-white/5 border-white/10 text-white' 
                      : 'bg-white border-gray-300 text-gray-900'
                  }`}
                >
                  <option value="">选择模板...</option>
                  {templates.map(t => (
                    <option key={t.name} value={t.pattern}>{t.name}</option>
                  ))}
                </select>
              </div>
              
              <div className="space-y-1.5">
                <label className={`text-[10px] font-medium ${isDark ? 'text-[#94a3b8]' : 'text-gray-600'}`}>
                  正则表达式
                </label>
                <input 
                  type="text" 
                  value={regexPattern} 
                  onChange={(e) => setRegexPattern(e.target.value)} 
                  placeholder="如：ORD\d{14} 或 \d{4}-\d{4}-\d{4}"
                  className={`h-9 text-[11px] font-mono rounded-md border px-3 w-full transition-colors ${
                    isDark 
                      ? 'bg-white/5 border-white/10 text-[#05c4a5] placeholder:text-white/30 focus:border-[#05c4a5] focus:outline-none' 
                      : 'bg-white border-gray-300 text-[#059669] placeholder:text-gray-400 focus:border-[#059669] focus:outline-none'
                  }`} 
                />
              </div>
            </div>
            
            <div className="flex justify-end gap-2 mt-4">
              <button 
                onClick={() => setShowRegexModal(false)} 
                className={`py-2 px-4 rounded-lg text-[11px] font-medium transition-colors ${
                  isDark ? 'bg-white/10 text-[#94a3b8] hover:bg-white/20' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                取消
              </button>
              <button 
                onClick={() => {
                  if (regexPattern.trim()) {
                    handleRegexGenerate()
                    setShowRegexModal(false)
                  }
                }} 
                disabled={isGenerating || !regexPattern.trim()}
                className={`py-2 px-4 rounded-lg text-[11px] font-medium transition-all flex items-center gap-1.5 ${
                  isDark 
                    ? 'bg-gradient-to-r from-[#5a5eff] to-[#768dff] hover:shadow-lg hover:shadow-[#5a5eff]/25' 
                    : 'bg-gradient-to-r from-[#4a3df0] to-[#5a5eff] hover:shadow-lg hover:shadow-[#4a3df0]/25 text-white'
                } disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                <Wand2 className="w-3 h-3" />
                生成数据
              </button>
            </div>
          </div>
        </div>
      )}

      {/* SQL 导出弹窗 */}
      {showSqlModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className={`p-4 w-full max-w-2xl mx-4 max-h-[80vh] flex flex-col rounded-xl ${isDark ? 'glass-card' : 'bg-white shadow-2xl border border-gray-200'}`}>
            <div className="flex items-center justify-between mb-3">
              <h3 className={`text-sm font-bold flex items-center gap-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                <FileCode className="w-4 h-4 text-[#5a5eff]" />
                导出 SQL
              </h3>
              <button onClick={() => setShowSqlModal(false)} className={isDark ? 'text-[#94a3b8] hover:text-white' : 'text-gray-400 hover:text-gray-600'}>
                <X className="w-4 h-4" />
              </button>
            </div>
            
            <div className="flex items-center gap-2 mb-3">
              <label className={`text-[10px] ${isDark ? 'text-[#94a3b8]' : 'text-gray-500'}`}>表名:</label>
              <input
                type="text"
                value={sqlTableName}
                onChange={(e) => setSqlTableName(e.target.value.replace(/[^a-zA-Z0-9_]/g, ''))}
                className={`text-[10px] py-1 px-2 w-40 rounded ${isDark ? 'input-glass' : 'border border-gray-300 bg-gray-50'}`}
                placeholder="table_name"
              />
            </div>
            
            <div className={`flex-1 overflow-auto rounded-lg p-3 mb-3 ${isDark ? 'bg-black/30' : 'bg-gray-100'}`}>
              <pre className={`text-[10px] font-mono whitespace-pre-wrap ${isDark ? 'text-[#94a3b8]' : 'text-gray-700'}`}>
                {generateSQL()}
              </pre>
            </div>
            
            <div className="flex justify-end gap-2">
              <button onClick={() => setShowSqlModal(false)} className="btn-secondary py-1.5 px-3 text-[10px]">
                取消
              </button>
              <button
                onClick={() => { navigator.clipboard.writeText(generateSQL()); toast({ description: '已复制到剪贴板', variant: 'success' }); }}
                className="btn-secondary py-1.5 px-3 text-[10px]"
              >
                <Copy className="w-3 h-3 inline mr-1" />
                复制
              </button>
              <button onClick={handleDownloadSQL} className="btn-primary py-1.5 px-3 text-[10px]">
                <Download className="w-3 h-3 inline mr-1" />
                下载 .sql
              </button>
            </div>
          </div>
        </div>
      )}

      <footer className={`border-t py-3 px-4 ${isDark ? 'border-white/10' : 'border-gray-200 bg-white'}`}>
        <div className="max-w-6xl mx-auto text-center">
          <p className={`text-[10px] ${isDark ? 'text-[#94a3b8]' : 'text-gray-500'}`}>Made with <span className="text-[#ff6b4a]">♥</span> by 知微 & 千机</p>
        </div>
      </footer>
    </div>
  )
}

function App() {
  return (
    <ToastProvider>
      <AppContent />
    </ToastProvider>
  )
}

export default App
