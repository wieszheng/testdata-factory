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
  ChevronRight,
  Globe,
  MapPin,
  Calendar,
  CreditCard as BankCard,
  User,
  Link,
  AlertCircle
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
  { key: 'bank_card', label: '银行卡号', icon: <BankCard className="w-4 h-4" /> },
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

interface DataItem {
  [key: string]: string
}

interface GenerateResponse {
  success: boolean
  count: number
  types: string[]
  data: DataItem[]
}

function App() {
  const [count, setCount] = useState(10)
  const [selectedTypes, setSelectedTypes] = useState<string[]>(['phone', 'email', 'id_card'])
  const [data, setData] = useState<DataItem[]>([])
  const [columns, setColumns] = useState<string[]>([])
  const [copied, setCopied] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)

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
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          count,
          types: selectedTypes,
        }),
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const result: GenerateResponse = await response.json()
      setData(result.data)
      setColumns(result.types)
    } catch (err) {
      setError(err instanceof Error ? err.message : '生成失败，请检查后端服务')
      console.error('Generate error:', err)
    } finally {
      setIsGenerating(false)
    }
  }

  const handleCopy = () => {
    const text = data.map(row => 
      columns.map(col => row[col] || '').join('\t')
    ).join('\n')
    
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleExportCSV = () => {
    const headers = columns.map(c => TYPE_LABELS[c] || c)
    const rows = data.map(row => 
      columns.map(col => row[col] || '').join(',')
    )
    
    const csv = headers.join(',') + '\n' + rows.join('\n')
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `test_data_${Date.now()}.csv`
    a.click()
    URL.revokeObjectURL(url)
  }

  const handleExportJSON = () => {
    const json = JSON.stringify(data.map(row => {
      const item: Record<string, string> = {}
      columns.forEach(col => {
        item[TYPE_LABELS[col] || col] = row[col] || ''
      })
      return item
    }), null, 2)
    const blob = new Blob([json], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `test_data_${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="gradient-bg-warm">
      {/* 导航栏 */}
      <nav className="sticky top-0 z-50 backdrop-blur-xl bg-white/70 border-b border-pink-100/50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="icon-container">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold gradient-text">TestData Factory</h1>
                <p className="text-xs text-gray-400">让造数据变得可爱又轻松</p>
              </div>
            </div>

            <div className="hidden sm:flex items-center gap-6">
              <a href="#generator" className="text-sm text-gray-600 hover:text-pink-500 transition-colors">生成器</a>
              <a 
                href="http://localhost:8000/docs" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center gap-1.5 text-sm text-gray-600 hover:text-pink-500 transition-colors"
              >
                <Settings className="w-4 h-4" />
                API 文档
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="py-12 sm:py-16 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 badge-soft mb-6">
            <span className="text-sm">✨</span>
            <span>v0.1.0 MVP</span>
          </div>
          
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            <span className="gradient-text">智能测试数据</span>
            <span className="text-gray-800"> 一键生成</span>
          </h2>
          
          <p className="text-base text-gray-500 max-w-xl mx-auto">
            手机号、邮箱、身份证、IP、地址、银行卡...告别手写 SQL，让造数据成为享受
          </p>
        </div>
      </section>

      {/* 生成器 */}
      <section id="generator" className="pb-12 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto">
          {/* 配置卡片 */}
          <div className="card-clay p-6 sm:p-8 mb-6">
            {/* 数据类型选择 */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-3">
                选择数据类型
              </label>
              <div className="flex flex-wrap gap-2">
                {DATA_TYPES.map(type => (
                  <button
                    key={type.key}
                    onClick={() => toggleType(type.key)}
                    className={`inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                      selectedTypes.includes(type.key)
                        ? 'bg-gradient-to-r from-pink-500 to-purple-500 text-white shadow-lg'
                        : 'bg-white border-2 border-pink-200 text-gray-600 hover:border-pink-300'
                    }`}
                  >
                    {type.icon}
                    {type.label}
                  </button>
                ))}
              </div>
            </div>

            {/* 数量和生成按钮 */}
            <div className="flex flex-col sm:flex-row items-start sm:items-end gap-4">
              <div className="flex-1 w-full sm:max-w-[200px]">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  生成数量
                </label>
                <input
                  type="number"
                  value={count}
                  onChange={(e) => setCount(Math.max(1, Math.min(1000, parseInt(e.target.value) || 1)))}
                  min={1}
                  max={1000}
                  className="input-soft text-center text-lg font-semibold"
                />
                <p className="text-xs text-gray-400 mt-1.5">支持 1-1000 条</p>
              </div>
              
              <button 
                onClick={handleGenerate}
                disabled={isGenerating || selectedTypes.length === 0}
                className="btn-primary w-full sm:w-auto flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isGenerating ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    生成中...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    生成数据
                  </>
                )}
              </button>
            </div>

            {/* 错误提示 */}
            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm text-red-600">{error}</p>
                </div>
              </div>
            )}
          </div>

          {/* 结果展示 */}
          {data.length > 0 && (
            <div className="card-clay overflow-hidden">
              {/* 工具栏 */}
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 sm:p-6 border-b border-pink-100/50 bg-gradient-to-r from-pink-50/50 to-purple-50/50">
                <div>
                  <h3 className="font-bold text-gray-800">生成结果</h3>
                  <p className="text-sm text-gray-500 mt-0.5">已生成 {data.length} 条数据，{columns.length} 个字段</p>
                </div>
                
                <div className="flex flex-wrap gap-2">
                  <button 
                    onClick={handleCopy}
                    className="px-4 py-2 bg-white border border-pink-200 rounded-lg text-sm font-medium text-pink-600 hover:bg-pink-50 transition-colors flex items-center gap-1.5"
                  >
                    {copied ? (
                      <>
                        <Check className="w-4 h-4 text-green-500" />
                        已复制
                      </>
                    ) : (
                      <>
                        <Copy className="w-4 h-4" />
                        复制
                      </>
                    )}
                  </button>
                  <button 
                    onClick={handleExportCSV}
                    className="px-4 py-2 bg-white border border-pink-200 rounded-lg text-sm font-medium text-pink-600 hover:bg-pink-50 transition-colors flex items-center gap-1.5"
                  >
                    <Download className="w-4 h-4" />
                    CSV
                  </button>
                  <button 
                    onClick={handleExportJSON}
                    className="px-4 py-2 bg-white border border-purple-200 rounded-lg text-sm font-medium text-purple-600 hover:bg-purple-50 transition-colors flex items-center gap-1.5"
                  >
                    <Download className="w-4 h-4" />
                    JSON
                  </button>
                </div>
              </div>

              {/* 数据表格 */}
              <div className="overflow-x-auto">
                <table className="table-soft">
                  <thead>
                    <tr>
                      {columns.map(col => (
                        <th key={col}>
                          {TYPE_LABELS[col] || col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {data.map((row, index) => (
                      <tr key={index}>
                        {columns.map(col => (
                          <td key={col} className={col === 'url' ? 'max-w-[200px] truncate' : ''}>
                            {row[col] || '-'}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* 功能预告 */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="card-clay p-5">
              <div className="flex items-center gap-3 mb-2">
                <div className="p-2 bg-gradient-to-br from-pink-400 to-purple-400 rounded-lg">
                  <Wand2 className="w-4 h-4 text-white" />
                </div>
                <h3 className="font-bold text-gray-800">自定义规则</h3>
              </div>
              <p className="text-sm text-gray-500">支持正则表达式，自由定义数据格式</p>
              <div className="mt-2 text-xs text-pink-500 font-medium">即将推出 →</div>
            </div>

            <div className="card-clay p-5">
              <div className="flex items-center gap-3 mb-2">
                <div className="p-2 bg-gradient-to-br from-cyan-400 to-blue-400 rounded-lg">
                  <Database className="w-4 h-4 text-white" />
                </div>
                <h3 className="font-bold text-gray-800">数据库逆向</h3>
              </div>
              <p className="text-sm text-gray-500">连接数据库，自动生成关联数据</p>
              <div className="mt-2 text-xs text-cyan-500 font-medium">Phase 2 →</div>
            </div>
          </div>
        </div>
      </section>

      {/* 页脚 */}
      <footer className="border-t border-pink-100/50 bg-white/50 py-6 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto text-center">
          <p className="text-sm text-gray-400">
            Made with <span className="text-pink-400">💖</span> by 知微 & 千机
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
