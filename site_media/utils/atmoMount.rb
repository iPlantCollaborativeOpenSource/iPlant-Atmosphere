#!/bin/env ruby

require 'net/http'
require 'net/https'
require 'uri'
require 'rubygems'
require 'json'

class Foo 

  def resourceRequest(userid,password)
    uri = URI.parse(@atmo_address)
    http = Net::HTTP.new(uri.host,uri.port)
    http.use_ssl = true if uri.scheme == "https"
    # Ha! Ha! Ha!
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE
    path = "/auth"
    headers = { "X_AUTH_USER" => userid, "X_AUTH_KEY" => password, "Content-type" => "application/x-www-form-urlencoded", "Accept" => "text/plain"}
    # Get request -> so the host can set his cookies
    resp, data = http.get(path, headers)
    #puts resp.message
    resp.each {|key, val| puts key + ' = ' + val}
    #puts data
  end


  def getAvailableVolumeList()
    uri = URI.parse(@api_server)
    http = Net::HTTP.new(uri.host,uri.port)
    http.use_ssl = true if uri.scheme == "https"
    # Ha! Ha! Ha!
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE
    path = uri.path+"/getVolumeList/" 
    headers = { 
      "Content-type" => "application/x-www-form-urlencoded",
      "Accept" => "text/plain",
      "X-Auth-User" => @atmo_credential['userid'],
      "X-Auth-Token" => @token,
      "X-Api-Server" => @api_server,
      "X-Api-Version" => "v1"
    }
    resp, data = http.get(path, headers)
    if JSON.parse(data)['result']['code'] == "success" 
      JSON.parse(data)['result']['value'].each { |a|
        if a['status'] == "available"
          p a['id']
        end
      }
    end
  end

  def getToken()
    userid = @atmo_credential['userid']
    password = @atmo_credential['password']
    uri = URI.parse(@atmo_address)
    http = Net::HTTP.new(uri.host,uri.port)
    http.use_ssl = true if uri.scheme == "https"
    # Ha! Ha! Ha!
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE
    path = "/auth"
    headers = { "X_AUTH_USER" => userid, "X_AUTH_KEY" => password, "Content-type" => "application/x-www-form-urlencoded", "Accept" => "text/plain"}
    # Get request -> so the host can set his cookies
    resp, data = http.get(path, headers)
    if (resp.code == "200") and (resp.message == "OK")
      @token = resp['x-auth-token']
      @api_server = resp['x-server-management-url']
    end
  end

  def printExplantion()
    puts "Mount your persistence storage"
  end

  def attacheVolume()
  end

  def detacheVolume()
  end

  def mountVolume()
  end 

  def unmountVolume()
  end

  def getUsernameAndPassword() 
    begin
      puts "what is your atmosphere username?"
      print "> " 
      @atmo_credential['userid'] = $stdin.gets.chomp
      puts "waht is your atmosphere password?"
      system "stty -echo"
      print"> "
      @atmo_credential['password'] = $stdin.gets.chomp
      puts ""
    rescue NoMethodError, Interrupt
      system "stty echo"
      exit
    end
  end

  def askMenu()
    puts "What do you want?"
    puts "[1] Attaching volume"
    puts "[2] Detaching volume"
    print "> (1,2,q(quit)) "
    selection = gets.chomp
    if selection == "1"
      getUsernameAndPassword()
      getToken()
      getAvailableVolumeList()
    elsif selection == "2"
      p "hi"
    elsif selection == "q"
      system "Stty echo"
      puts "Bye"
      exit
    else
      puts "Invalid input"
      puts "\n"
      askMenu()
    end
  end 


  def main()

    # only root or with sudo can do this script
    #raise 'Must run as root' unless Process.uid == 0
    if Process.uid != 0
      puts "Only root or with sudo command can run this script"
      puts "Please run as root or use 'sudo atmoMount'"
      puts ""
      exit
    end 

    @atmo_address = "https://atmo.iplantcollaborative.org"
    @atmo_credential = {}
    
    askMenu() 
  
    #getUsernameAndPassword()

    #sudoAccessCheck()
    #resourceRequest(@atmo_credential['userid'],@atmo_credential['password'])
    #getToken()
    #getAvailableVolumeList()
    system "stty echo"
  end

end



f = Foo.new
f.main()