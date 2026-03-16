import { useState, useEffect } from 'react'
import { 
  Sparkles, 
  Phone, 
  Mail, 
  CreditCard, 
  Download, 
  Copy, 
  Check,
  Settings,
  Database,
  Wand2,
  ChevronDown,
  Globe,
  MapPin,
  Calendar,
  User,
  Link,
  AlertCircle,
  Code,
  Moon,
  Zap
} from 'lucide-react'

const API_BASE = 'http://localhost:8000/api'

interface DataType {
  key: string
  label: string
  icon: React.ReactNode
}

const DATA_TYPES: DataType[] = [
  { key: 'phone', label: '手机号', icon: <Phone className="w-4 h-4" /> },
  { key: 'email', label: '邮箱', icon: <Mail className="w-4 h-4" /> },
  { key: 'id_card', label: '身份证号', icon: <CreditCard className="w-4 h-4" /> },
  { key: 'name', label: '姓名', icon: <User className="w-4 h-4" /> },
  { key: 'ip', label: 'IP地址', icon: <Globe className="w-4 h-4" /> },
  { key: 'address', label: '地址', icon: <MapPin className="w-4 h-4" /> },
  { key: 'date', label: '日期', icon: <Calendar className="w-4 h-4" /> },
  { key: 'bank_card', label: '银行卡号', icon: <CreditCard className="w-4 h-4" /> },
  { key: 'url', label: 'URL', icon: <Link className="w-4 h-4" /> },
]

const TYPE_LABELS: Record<string, string> = {
  phone: '手机号',
  email: '邮箱',
  id_card: '身份证号',
  name: '姓名',
  ip: 'IP地址',
  ipv6: 'IPv6地址',
  address: '地址',
  date: '日期',
  datetime: '日期时间',
  bank_card: '银行卡号',
  url: 'URL',
}

interface RegexTemplate {
  name: string
  pattern: string
}

interface DataItem {
  [key: string]: string
}

function App() {
  const [count, setCount] = useState(10)
  const [selectedTypes, setSelectedTypes] = useState<string[]>(['phone', 'email', 'id_card'])
  const [data, setData] = useState<DataItem[]>([])
  const [columns, setColumns] = useState<string[]>([])
  const [copied, setCopied] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  // 正则规则
  const [showRegex, setShowRegex] = useState(false)
  const [regexPattern, setRegexPattern] = useState('')
  const [regexName, setRegexName] = useState('自定义字段')
  const [templates, setTemplates] = useState<RegexTemplate[]>([])
  const [regexData, setRegexData] = useState<string[]>([])

  useEffect(() => {
    fetch(`${API_BASE}/templates`)
      .then(res => res.json())
      .then(result => setTemplates(result.templates || []))
      .catch(() => {})
  }, [])

  const toggleType = (key: string) => {
    setSelectedTypes(prev => 
      prev.includes(key) 
        ? prev.filter(t => t !== key)
        : [...prev, key]
    )
  }

  const handleGenerate = async () => {
    if (selectedTypes.length === 0) {
      setError('请至少选择一种数据类型')
      return
    }

    setIsGenerating(true)
    setError(null)
    
    try {
      const response = await fetch(`${API_BASE}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ count, types: selectedTypes }),
      })
      
      const result = await response.json()
      setData(result.data)
      setColumns(result.types)
      setRegexData([])
    } catch (err) {
      setError('生成失败，请检查后端服务')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleRegexGenerate = async () => {
    if (!regexPattern.trim()) {
      setError('请输入正则表达式')
      return
    }

    setIsGenerating(true)
    setError(null)
    
    try {
      const response = await fetch(`${API_BASE}/regex`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ count, pattern: regexPattern, name: regexName }),
      })
      
      const result = await response.json()
      if (result.success) {
        setRegexData(result.data)
        setData([])
        setColumns([])
      } else {
        setError('正则表达式格式错误')
      }
    } catch (err) {
      setError('生成失败')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleCopy = () => {
    let text = ''
    if (data.length > 0) {
      text = data.map(row => columns.map(col => row[col] || '').join('\t')).join('\n')
    } else if (regexData.length > 0) {
      text = regexData.join('\n')
    }
    
    if (text) {
      navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const handleExportCSV = () => {
    let csv = ''
    if (data.length > 0) {
      const headers = columns.map(c => TYPE_LABELS[c] || c)
      csv = headers.join(',') + '\n' + data.map(row => columns.map(col => row[col] || '').join(',')).join('\n')
    } else if (regexData.length > 0) {
      csv = regexName + '\n' + regexData.join('\n')
    }
    
    if (csv) {
      const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `test_data_${Date.now()}.csv`
      a.click()
      URL.revokeObjectURL(url)
    }
  }

  const handleExportJSON = () => {
    let json = ''
    if (data.length > 0) {
      json = JSON.stringify(data.map(row => {
        const item: Record<string, string> = {}
        columns.forEach(col => { item[TYPE_LABELS[col] || col] = row[col] || '' })
        return item
      }), null, 2)
    } else if (regexData.length > 0) {
      json = JSON.stringify(regexData.map(v => ({ [regexName]: v })), null, 2)
    }
    
    if (json) {
      const blob = new Blob([json], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `test_data_${Date.now()}.json`
      a.click()
      URL.revokeObjectURL(url)
    }
  }

  return (
    <div className="min-h-screen">
      {/* 背景装饰 */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-[#ff6b4a] opacity-10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-[#5a5eff] opacity-10 rounded-full blur-3xl" />
        <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-[#05c4a5] opacity-5 rounded-full blur-3xl" />
      </div>

      {/* 导航栏 */}
      <nav className="sticky top-0 z-50 backdrop-blur-xl bg-[#0f1419]/80 border-b border-white/10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="icon-glow animate-glow">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold gradient-text-warm">TestData Factory</h1>
                <p className="text-xs text-[#94a3b8]">智能测试数据生成器</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <a 
                href="http://localhost:8000/docs" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-sm text-[#94a3b8] hover:text-[#ff6b4a] transition-colors flex items-center gap-1.5"
              >
                <Settings className="w-4 h-4" />
                <span className="hidden sm:inline">API</span>
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative py-6 sm:py-8 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="badge-glow mb-3">
            <Moon className="w-3.5 h-3.5" />
            <span>v0.1.0 MVP</span>
          </div>
          
          <h2 className="text-2xl sm:text-3xl font-bold mb-2">
            <span className="gradient-text-warm">测试数据</span>
            <span className="text-white"> 一键生成</span>
          </h2>
          
          <p className="text-sm text-[#94a3b8]">
            手机号、邮箱、身份证、IP、银行卡...支持自定义正则规则
          </p>
        </div>
      </section>

      {/* 生成器 */}
      <section id="generator" className="relative pb-8 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto">
          {/* 主卡片 */}
          <div className="glass-card p-4 sm:p-6 mb-4 animate-glow">
            {/* 数据类型选择 */}
            <div className="mb-4">
              <label className="block text-xs font-medium text-[#94a3b8] mb-2">
                选择数据类型
              </label>
              <div className="flex flex-wrap gap-1.5">
                {DATA_TYPES.map(type => (
                  <button
                    key={type.key}
                    onClick={() => toggleType(type.key)}
                    className={`type-btn text-xs py-1.5 px-3 ${selectedTypes.includes(type.key) ? 'active' : ''}`}
                  >
                    {type.icon}
                    {type.label}
                  </button>
                ))}
              </div>
            </div>

            {/* 正则规则展开 */}
            <div className="mb-4">
              <button
                onClick={() => setShowRegex(!showRegex)}
                className="flex items-center gap-2 text-xs font-medium text-[#5a5eff] hover:text-[#768dff] transition-colors"
              >
                <Code className="w-3.5 h-3.5" />
                自定义正则规则
                <ChevronDown className={`w-3.5 h-3.5 transition-transform ${showRegex ? 'rotate-180' : ''}`} />
              </button>
              
              {showRegex && (
                <div className="mt-3 p-3 rounded-lg bg-white/5 border border-white/10">
                  <div className="grid gap-3 sm:grid-cols-2">
                    <div>
                      <label className="block text-xs font-medium text-[#94a3b8] mb-1">字段名称</label>
                      <input
                        type="text"
                        value={regexName}
                        onChange={(e) => setRegexName(e.target.value)}
                        className="input-glass text-xs py-1.5"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-[#94a3b8] mb-1">预定义模板</label>
                      <select
                        value={regexPattern}
                        onChange={(e) => {
                          setRegexPattern(e.target.value)
                          const template = templates.find(t => t.pattern === e.target.value)
                          if (template) setRegexName(template.name)
                        }}
                        className="input-glass text-xs py-1.5"
                      >
                        <option value="">选择模板...</option>
                        {templates.map(t => (
                          <option key={t.name} value={t.pattern}>{t.name}</option>
                        ))}
                      </select>
                    </div>
                  </div>
                  
                  <div className="mt-2">
                    <label className="block text-xs font-medium text-[#94a3b8] mb-1">正则表达式</label>
                    <input
                      type="text"
                      value={regexPattern}
                      onChange={(e) => setRegexPattern(e.target.value)}
                      placeholder="例如: ORD\d{14}"
                      className="input-glass text-xs font-mono"
                    />
                  </div>
                  
                  <button
                    onClick={handleRegexGenerate}
                    disabled={isGenerating || !regexPattern.trim()}
                    className="mt-3 px-3 py-1.5 bg-gradient-to-r from-[#5a5eff] to-[#768dff] text-white rounded-lg text-xs font-medium disabled:opacity-50"
                  >
                    <Wand2 className="w-3 h-3 inline mr-1" />
                    生成正则数据
                  </button>
                </div>
              )}
            </div>

            <div className="divider-glow mb-4" />

            {/* 数量和生成按钮 */}
            <div className="flex items-center gap-2">
              <div className="w-[80px]">
                <label className="block text-xs font-medium text-[#94a3b8] mb-1">数量</label>
                <input
                  type="number"
                  value={count}
                  onChange={(e) => setCount(Math.max(1, Math.min(1000, parseInt(e.target.value) || 1)))}
                  min={1}
                  max={1000}
                  className="input-glass text-center text-sm font-semibold py-1.5 px-2"
                />
              </div>
              
              <button 
                onClick={handleGenerate}
                disabled={isGenerating || selectedTypes.length === 0}
                className="btn-primary flex items-center justify-center gap-1.5 disabled:opacity-50 mt-4"
              >
                {isGenerating ? (
                  <>
                    <div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    生成中...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-3 h-3" />
                    生成
                  </>
                )}
              </button>
            </div>

            {error && (
              <div className="mt-3 p-3 bg-red-500/10 border border-red-500/30 rounded-lg flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-red-400" />
                <p className="text-xs text-red-400">{error}</p>
              </div>
            )}
          </div>

          {/* 结果展示 */}
          {(data.length > 0 || regexData.length > 0) && (
            <div className="glass-card overflow-hidden mb-4">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 p-3 sm:p-4 border-b border-white/10">
                <div>
                  <h3 className="font-bold text-white text-sm">生成结果</h3>
                  <p className="text-xs text-[#94a3b8]">
                    {data.length > 0 
                      ? `${data.length} 条数据，${columns.length} 个字段`
                      : `${regexData.length} 条 ${regexName}`
                    }
                  </p>
                </div>
                
                <div className="flex gap-1.5">
                  <button onClick={handleCopy} className="btn-secondary py-1.5 px-2.5 text-xs">
                    {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
                  </button>
                  <button onClick={handleExportCSV} className="btn-secondary py-1.5 px-2.5 text-xs">
                    <Download className="w-3.5 h-3.5" /> CSV
                  </button>
                  <button onClick={handleExportJSON} className="btn-secondary py-1.5 px-2.5 text-xs">
                    <Download className="w-3.5 h-3.5" /> JSON
                  </button>
                </div>
              </div>

              <div className="overflow-x-auto max-h-[400px] overflow-y-auto">
                {data.length > 0 ? (
                  <table className="table-glass">
                    <thead className="sticky top-0">
                      <tr>
                        {columns.map(col => <th key={col} className="text-xs py-2">{TYPE_LABELS[col] || col}</th>)}
                      </tr>
                    </thead>
                    <tbody>
                      {data.map((row, i) => (
                        <tr key={i}>
                          {columns.map(col => <td key={col} className="text-xs py-2">{row[col] || '-'}</td>)}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <table className="table-glass">
                    <thead className="sticky top-0"><tr><th className="text-xs py-2">{regexName}</th></tr></thead>
                    <tbody>
                      {regexData.map((v, i) => <tr key={i}><td className="text-xs py-2">{v}</td></tr>)}
                    </tbody>
                  </table>
                )}
              </div>
            </div>
          )}

          {/* 功能预告 */}
          <div className="glass-card p-3 flex items-center gap-3">
            <div className="p-1.5 bg-gradient-to-br from-[#05c4a5] to-[#009e87] rounded-lg">
              <Database className="w-3.5 h-3.5 text-white" />
            </div>
            <div className="flex-1">
              <h3 className="font-bold text-white text-xs">数据库逆向</h3>
              <p className="text-xs text-[#94a3b8]">连接数据库，自动识别表结构</p>
            </div>
            <div className="text-xs text-[#05c4a5] font-medium">Phase 2</div>
          </div>
        </div>
      </section>

      {/* 页脚 */}
      <footer className="border-t border-white/10 py-4 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto text-center">
          <p className="text-xs text-[#94a3b8]">
            Made with <span className="text-[#ff6b4a]">♥</span> by 知微 & 千机
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
