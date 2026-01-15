import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api } from '../services/api'

const signupMotivations = [
  {
    title: "Start Your Journey",
    description: "Join StudyMate today and unlock a world of organized study materials. Your academic success begins here.",
    icon: "🌟"
  },
  {
    title: "Never Miss a Note",
    description: "Access all your study materials in one place. No more searching through multiple platforms or groups.",
    icon: "📖"
  },
  {
    title: "Study at Your Pace",
    description: "Download materials anytime, anywhere. Study when it's convenient for you, on any device.",
    icon: "⏰"
  },
  {
    title: "Connect with Excellence",
    description: "Join a community of students and educators dedicated to academic excellence and knowledge sharing.",
    icon: "🤝"
  },
  {
    title: "Achieve Your Goals",
    description: "With organized materials and easy access, focus on what matters most - your learning and success.",
    icon: "🎯"
  }
]

function SignUp() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [currentMotivation, setCurrentMotivation] = useState(0)

  // Auto-rotate motivations every 4 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentMotivation((prev) => (prev + 1) % signupMotivations.length)
    }, 4000)
    return () => clearInterval(interval)
  }, [])

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    setError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      setLoading(false)
      return
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters long')
      setLoading(false)
      return
    }

    try {
      const response = await api.register({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        first_name: formData.first_name,
        last_name: formData.last_name
      })
      
      const loginResponse = await api.login(null, formData.email, formData.password)
      
      localStorage.setItem('accessToken', loginResponse.access)
      localStorage.setItem('refreshToken', loginResponse.refresh)
      localStorage.setItem('isAuthenticated', 'true')
      localStorage.setItem('userRole', loginResponse.role || 'student')
      localStorage.setItem('username', loginResponse.username || formData.username)
      
      navigate('/student/dashboard')
    } catch (err) {
      setError(err.message || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-lg border-b border-gray-200/50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <Link to="/" className="flex items-center space-x-2">
              <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                StudyMate
              </h1>
            </Link>
            <div className="hidden md:flex items-center space-x-8">
              <a href="/#features" className="text-gray-700 hover:text-indigo-600 font-medium transition-colors">Features</a>
              <a href="/#structure" className="text-gray-700 hover:text-indigo-600 font-medium transition-colors">Structure</a>
              <a href="/#about" className="text-gray-700 hover:text-indigo-600 font-medium transition-colors">About</a>
            </div>
            <div className="flex items-center space-x-4">
              <Link to="/login" className="text-gray-700 hover:text-indigo-600 px-4 py-2 rounded-lg text-sm font-medium transition-all hover:bg-gray-100">
                Login
              </Link>
              <Link to="/signup" className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white px-6 py-2.5 rounded-lg text-sm font-semibold transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">
                Sign Up
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Split Screen Layout */}
      <div className="pt-20 min-h-screen flex">
        {/* Left Side - Motivational Content */}
        <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-purple-600 via-pink-600 to-indigo-600 items-center justify-center p-12 relative overflow-hidden">
          {/* Animated Background */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-20 left-20 w-72 h-72 bg-white rounded-full mix-blend-overlay filter blur-xl animate-blob"></div>
            <div className="absolute top-40 right-20 w-72 h-72 bg-white rounded-full mix-blend-overlay filter blur-xl animate-blob animation-delay-2000"></div>
            <div className="absolute bottom-20 left-40 w-72 h-72 bg-white rounded-full mix-blend-overlay filter blur-xl animate-blob animation-delay-4000"></div>
          </div>

          {/* Content Container - Positioned higher */}
          <div className="relative z-10 w-full max-w-lg -mt-20">
            {signupMotivations.map((motivation, index) => (
              <div
                key={index}
                className={`absolute inset-0 transition-opacity duration-1000 ${
                  index === currentMotivation ? 'opacity-100' : 'opacity-0'
                }`}
              >
                <div className="text-center text-white">
                  <div className="text-8xl mb-6 animate-bounce">
                    {motivation.icon}
                  </div>
                  <h3 className="text-4xl font-bold mb-4">
                    {motivation.title}
                  </h3>
                  <p className="text-xl text-white/90 leading-relaxed">
                    {motivation.description}
                  </p>
                </div>
              </div>
            ))}

            {/* Progress Indicators */}
            <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-2">
              {signupMotivations.map((_, index) => (
                <div
                  key={index}
                  className={`h-2 rounded-full transition-all duration-300 ${
                    index === currentMotivation
                      ? 'w-8 bg-white'
                      : 'w-2 bg-white/50'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Right Side - Sign Up Form */}
        <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
          <div className="w-full max-w-md space-y-8">
            <div className="text-center lg:text-left">
              <h2 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-2">
                Create Account
              </h2>
              <p className="text-gray-600">Sign up to start your StudyMate journey</p>
            </div>

            <div className="bg-white rounded-2xl shadow-2xl p-8 border border-gray-100">
              <form onSubmit={handleSubmit} className="space-y-6">
                {error && (
                  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                    {error}
                  </div>
                )}

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="first_name" className="block text-sm font-semibold text-gray-700 mb-2">
                      First Name
                    </label>
                    <input
                      id="first_name"
                      name="first_name"
                      type="text"
                      required
                      value={formData.first_name}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                      placeholder="First name"
                    />
                  </div>

                  <div>
                    <label htmlFor="last_name" className="block text-sm font-semibold text-gray-700 mb-2">
                      Last Name
                    </label>
                    <input
                      id="last_name"
                      name="last_name"
                      type="text"
                      required
                      value={formData.last_name}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                      placeholder="Last name"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="username" className="block text-sm font-semibold text-gray-700 mb-2">
                    Username
                  </label>
                  <input
                    id="username"
                    name="username"
                    type="text"
                    required
                    value={formData.username}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                    placeholder="Choose a username"
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2">
                    Email
                  </label>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    required
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                    placeholder="Enter your email"
                  />
                </div>

                <div>
                  <label htmlFor="password" className="block text-sm font-semibold text-gray-700 mb-2">
                    Password
                  </label>
                  <input
                    id="password"
                    name="password"
                    type="password"
                    required
                    value={formData.password}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                    placeholder="Create a password"
                  />
                </div>

                <div>
                  <label htmlFor="confirmPassword" className="block text-sm font-semibold text-gray-700 mb-2">
                    Confirm Password
                  </label>
                  <input
                    id="confirmPassword"
                    name="confirmPassword"
                    type="password"
                    required
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                    placeholder="Confirm your password"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white py-3 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                >
                  {loading ? 'Creating Account...' : 'Sign Up'}
                </button>
              </form>

              <div className="mt-6 text-center">
                <p className="text-sm text-gray-600">
                  Already have an account?{' '}
                  <Link to="/login" className="text-indigo-600 hover:text-indigo-700 font-medium">
                    Sign In
                  </Link>
                </p>
                <button
                  onClick={() => navigate('/')}
                  className="mt-2 text-indigo-600 hover:text-indigo-700 text-sm font-medium"
                >
                  ← Back to Home
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SignUp
