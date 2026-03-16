import { useState, useEffect } from 'react'
import { 
  Sparkles, Phone, Mail, CreditCard, Download, Copy, Check,
  Settings, Database, Wand2, ChevronDown, Globe, MapPin,
  Calendar, User, Link, AlertCircle, Code, Building, Briefcase,
  DollarSign, Palette, Fingerprint, Key, FileText
} from 'lucide-react'

const API_BASE = 'http://localhost:8000/api'

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

function App() {
  const [count, setCount] = useState(10)
  const [selectedTypes, setSelectedTypes] = useState<string[]>(['phone', 'email', 'name'])
  const [data, setData] = useState<DataItem[]>([])
  const [columns, setColumns] = useState<string[]>([])
  const [copied, setCopied] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
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
      prev.includes(key) ? prev.filter(t => t !== key) : [...prev, key]
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
    } catch {
      setError('生成失败')
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
    } catch {
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
      csv = columns.map(c => TYPE_LABELS[c] || c).join(',') + '\n' +
        data.map(row => columns.map(col => row[col] || '').join(',')).join('\n')
    } else if (regexData.length > 0) {
      csv = regexName + '\n' + regexData.join('\n')
    }
    if (csv) {
      const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url; a.download = `test_data_${Date.now()}.csv`; a.click()
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
      a.href = url; a.download = `test_data_${Date.now()}.json`; a.click()
      URL.revokeObjectURL(url)
    }
  }

  return (
    <div className="min-h-screen">
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-[#ff6b4a] opacity-10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-[#5a5eff] opacity-10 rounded-full blur-3xl" />
      </div>

      <nav className="sticky top-0 z-50 backdrop-blur-xl bg-[#0f1419]/80 border-b border-white/10">
        <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="icon-glow animate-glow p-1.5">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <div>
              <h1 className="text-sm font-bold gradient-text-warm">TestData Factory</h1>
              <p className="text-[10px] text-[#94a3b8]">智能测试数据生成器</p>
            </div>
          </div>
          <a href="http://localhost:8000/docs" target="_blank" className="text-[10px] text-[#94a3b8] hover:text-[#ff6b4a] flex items-center gap-1">
            <Settings className="w-3 h-3" /> API
          </a>
        </div>
      </nav>

      <section className="py-4 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-xl font-bold mb-1">
            <span className="gradient-text-warm">测试数据</span>
            <span className="text-white"> 一键生成</span>
          </h2>
          <p className="text-xs text-[#94a3b8]">17 种数据类型 · 自定义正则 · 导出 CSV/JSON</p>
        </div>
      </section>

      <section className="pb-8 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="glass-card p-3 sm:p-4 mb-3 animate-glow">
            <div className="mb-3">
              <label className="block text-[10px] font-medium text-[#94a3b8] mb-1.5">选择数据类型</label>
              <div className="flex flex-wrap gap-1">
                {DATA_TYPES.map(type => (
                  <button key={type.key} onClick={() => toggleType(type.key)}
                    className={`type-btn text-[10px] py-1 px-2 ${selectedTypes.includes(type.key) ? 'active' : ''}`}>
                    {type.icon}
                    <span className="ml-0.5">{type.label}</span>
                  </button>
                ))}
              </div>
            </div>

            <div className="mb-3">
              <button onClick={() => setShowRegex(!showRegex)}
                className="flex items-center gap-1.5 text-[10px] text-[#5a5eff] hover:text-[#768dff]">
                <Code className="w-3 h-3" />
                自定义正则
                <ChevronDown className={`w-3 h-3 transition-transform ${showRegex ? 'rotate-180' : ''}`} />
              </button>
              
              {showRegex && (
                <div className="mt-2 p-2 rounded-lg bg-white/5 border border-white/10 grid gap-2 sm:grid-cols-2">
                  <input type="text" value={regexName} onChange={(e) => setRegexName(e.target.value)}
                    placeholder="字段名" className="input-glass text-[10px] py-1" />
                  <select value={regexPattern} onChange={(e) => { setRegexPattern(e.target.value); const t = templates.find(t => t.pattern === e.target.value); if (t) setRegexName(t.name) }}
                    className="input-glass text-[10px] py-1">
                    <option value="">选择模板...</option>
                    {templates.map(t => <option key={t.name} value={t.pattern}>{t.name}</option>)}
                  </select>
                  <input type="text" value={regexPattern} onChange={(e) => setRegexPattern(e.target.value)}
                    placeholder="正则: ORD\d{14}" className="input-glass text-[10px] font-mono sm:col-span-2" />
                  <button onClick={handleRegexGenerate} disabled={isGenerating || !regexPattern.trim()}
                    className="px-2 py-1 bg-gradient-to-r from-[#5a5eff] to-[#768dff] text-white rounded text-[10px] font-medium disabled:opacity-50 sm:col-span-2">
                    <Wand2 className="w-3 h-3 inline mr-1" />生成
                  </button>
                </div>
              )}
            </div>

            <div className="divider-glow mb-3" />

            <div className="flex items-end gap-2">
              <div className="w-[70px]">
                <label className="block text-[10px] text-[#94a3b8] mb-1">数量</label>
                <input type="number" value={count} onChange={(e) => setCount(Math.max(1, Math.min(1000, parseInt(e.target.value) || 1)))}
                  min={1} max={1000} className="input-glass text-center text-xs font-semibold py-1 px-1" />
              </div>
              <button onClick={handleGenerate} disabled={isGenerating || selectedTypes.length === 0}
                className="btn-primary flex items-center justify-center gap-1 disabled:opacity-50 h-[28px] px-3 text-[10px]">
                {isGenerating ? <>
                  <div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  生成中
                </> : <>
                  <Sparkles className="w-3 h-3" />生成
                </>}
              </button>
            </div>

            {error && (
              <div className="mt-2 p-2 bg-red-500/10 border border-red-500/30 rounded flex items-center gap-2">
                <AlertCircle className="w-3 h-3 text-red-400" />
                <p className="text-[10px] text-red-400">{error}</p>
              </div>
            )}
          </div>

          {(data.length > 0 || regexData.length > 0) && (
            <div className="glass-card overflow-hidden mb-3">
              <div className="flex items-center justify-between gap-2 p-2 border-b border-white/10">
                <div>
                  <h3 className="font-bold text-white text-xs">结果</h3>
                  <p className="text-[10px] text-[#94a3b8]">
                    {data.length > 0 ? `${data.length} 条 · ${columns.length} 字段` : `${regexData.length} 条`}
                  </p>
                </div>
                <div className="flex gap-1">
                  <button onClick={handleCopy} className="btn-secondary py-1 px-1.5">
                    {copied ? <Check className="w-3 h-3 text-green-400" /> : <Copy className="w-3 h-3" />}
                  </button>
                  <button onClick={handleExportCSV} className="btn-secondary py-1 px-1.5 text-[10px]">
                    <Download className="w-3 h-3" />CSV
                  </button>
                  <button onClick={handleExportJSON} className="btn-secondary py-1 px-1.5 text-[10px]">
                    <Download className="w-3 h-3" />JSON
                  </button>
                </div>
              </div>

              <div className="overflow-x-auto max-h-[350px] overflow-y-auto">
                {data.length > 0 ? (
                  <table className="table-glass">
                    <thead className="sticky top-0">
                      <tr>{columns.map(col => <th key={col} className="text-[10px] py-1.5 px-2">{TYPE_LABELS[col] || col}</th>)}</tr>
                    </thead>
                    <tbody>
                      {data.map((row, i) => (
                        <tr key={i}>{columns.map(col => <td key={col} className="text-[10px] py-1.5 px-2">{row[col] || '-'}</td>)}</tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <table className="table-glass">
                    <thead className="sticky top-0"><tr><th className="text-[10px] py-1.5 px-2">{regexName}</th></tr></thead>
                    <tbody>
                      {regexData.map((v, i) => <tr key={i}><td className="text-[10px] py-1.5 px-2">{v}</td></tr>)}
                    </tbody>
                  </table>
                )}
              </div>
            </div>
          )}

          <div className="glass-card p-2 flex items-center gap-2">
            <div className="p-1 bg-gradient-to-br from-[#05c4a5] to-[#009e87] rounded">
              <Database className="w-3 h-3 text-white" />
            </div>
            <div className="flex-1">
              <h3 className="font-bold text-white text-[10px]">数据库逆向</h3>
              <p className="text-[10px] text-[#94a3b8]">连接数据库，自动生成关联数据</p>
            </div>
            <div className="text-[10px] text-[#05c4a5] font-medium">Phase 2</div>
          </div>
        </div>
      </section>

      <footer className="border-t border-white/10 py-3 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <p className="text-[10px] text-[#94a3b8]">Made with <span className="text-[#ff6b4a]">♥</span> by 知微 & 千机</p>
        </div>
      </footer>
    </div>
  )
}

export default App
